from __future__ import annotations

import json
import subprocess
from pathlib import Path

from .utils import find_ffmpeg, fmt_time


DEFAULT_PROMPT = (
    "Course or internet video. Preserve domain terms, names, frameworks, technical terms, "
    "and mixed-language speech when possible."
)


def extract_audio(media: Path, out_dir: Path) -> Path:
    ffmpeg = find_ffmpeg()
    if not ffmpeg:
        raise SystemExit("ffmpeg or imageio-ffmpeg is required to extract audio.")
    out_dir.mkdir(parents=True, exist_ok=True)
    audio = out_dir / "audio-16khz.wav"
    subprocess.run(
        [
            ffmpeg,
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(media),
            "-vn",
            "-ac",
            "1",
            "-ar",
            "16000",
            str(audio),
        ],
        check=True,
    )
    return audio


def transcribe_local(
    media: Path,
    out_dir: Path,
    model_size: str = "small",
    language: str | None = None,
    initial_prompt: str = DEFAULT_PROMPT,
) -> list[dict]:
    try:
        from faster_whisper import WhisperModel
    except ImportError as exc:
        raise SystemExit("Install local transcription with: python -m pip install faster-whisper") from exc

    audio = extract_audio(media, out_dir)
    model = WhisperModel(model_size, device="auto", compute_type="auto")
    segments, _info = model.transcribe(
        str(audio),
        language=language,
        initial_prompt=initial_prompt,
        vad_filter=True,
        word_timestamps=False,
    )
    rows: list[dict] = []
    for segment in segments:
        text = " ".join(segment.text.split())
        if text:
            rows.append({"start": float(segment.start), "end": float(segment.end), "text": text})
    write_transcript(rows, out_dir)
    return rows


def write_transcript(segments: list[dict], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "transcript.segments.json").write_text(
        json.dumps(segments, indent=2), encoding="utf-8"
    )
    md = [f"[{fmt_time(s['start'])}] {s['text']}" for s in segments]
    (out_dir / "transcript.md").write_text("\n\n".join(md), encoding="utf-8")
    quotes = []
    for s in segments:
        if 40 <= len(s["text"]) <= 220:
            quotes.append(f"- {fmt_time(s['start'])} - \"{s['text']}\"")
    (out_dir / "quote-candidates.md").write_text("\n".join(quotes), encoding="utf-8")
