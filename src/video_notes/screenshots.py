from __future__ import annotations

import json
import subprocess
from pathlib import Path

from PIL import Image

from .exceptions import DependencyMissingError
from .utils import find_ffmpeg, fmt_time


def extract_frames(video: Path, out_dir: Path, interval: int = 30) -> list[Path]:
    ffmpeg = find_ffmpeg()
    if not ffmpeg:
        raise DependencyMissingError("ffmpeg or imageio-ffmpeg is required to extract frames.")
    frames = out_dir / "frames"
    frames.mkdir(parents=True, exist_ok=True)
    duration = probe_duration(video)
    paths: list[Path] = []
    for seconds in range(0, max(int(duration), 1), max(interval, 1)):
        stamp = fmt_time(seconds).replace(":", "-")
        target = frames / f"{stamp}.jpg"
        subprocess.run(
            [
                ffmpeg,
                "-y",
                "-hide_banner",
                "-loglevel",
                "error",
                "-ss",
                str(seconds),
                "-i",
                str(video),
                "-frames:v",
                "1",
                "-update",
                "1",
                "-q:v",
                "2",
                str(target),
            ],
            check=True,
        )
        normalize_image(target)
        if target.exists():
            paths.append(target)
    (out_dir / "frames.json").write_text(
        json.dumps([str(p) for p in paths], indent=2), encoding="utf-8"
    )
    return paths


def probe_duration(video: Path) -> float:
    ffmpeg = find_ffmpeg()
    result = subprocess.run([ffmpeg, "-i", str(video)], capture_output=True, text=True)
    marker = "Duration: "
    if marker not in result.stderr:
        return 0.0
    value = result.stderr.split(marker, 1)[1].split(",", 1)[0]
    hh, mm, ss = value.split(":")
    return int(hh) * 3600 + int(mm) * 60 + float(ss)


def normalize_image(path: Path) -> None:
    img = Image.open(path).convert("RGB")
    img.save(path, "JPEG", quality=88, optimize=True)


def select_representative_frames(frames: list[Path], max_count: int = 12) -> list[Path]:
    if len(frames) <= max_count:
        return frames
    scored = score_scene_changes(frames)
    if not scored:
        return select_evenly_spaced_frames(frames, max_count=max_count)

    chosen = {0}
    ranked = sorted(scored, key=lambda item: item[1], reverse=True)
    for idx, score in ranked:
        if len(chosen) >= max_count:
            break
        if score > 0:
            chosen.add(idx)

    if len(chosen) < max_count:
        for frame in select_evenly_spaced_frames(frames, max_count=max_count):
            chosen.add(frames.index(frame))
            if len(chosen) >= max_count:
                break

    return [frames[idx] for idx in sorted(chosen)]


def select_evenly_spaced_frames(frames: list[Path], max_count: int = 12) -> list[Path]:
    if len(frames) <= max_count:
        return frames
    step = len(frames) / max_count
    return [frames[int(i * step)] for i in range(max_count)]


def score_scene_changes(frames: list[Path]) -> list[tuple[int, float]]:
    scores: list[tuple[int, float]] = []
    previous = None
    for idx, frame in enumerate(frames):
        signature = image_signature(frame)
        if signature is None:
            return []
        if previous is not None:
            scores.append((idx, signature_distance(previous, signature)))
        previous = signature
    return scores


def image_signature(path: Path) -> list[int] | None:
    try:
        with Image.open(path) as img:
            gray = img.convert("L").resize((8, 8))
            return list(gray.getdata())
    except OSError:
        return None


def signature_distance(first: list[int], second: list[int]) -> float:
    if len(first) != len(second):
        return 0.0
    return sum(abs(a - b) for a, b in zip(first, second)) / len(first)
