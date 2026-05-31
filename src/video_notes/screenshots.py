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
    step = len(frames) / max_count
    return [frames[int(i * step)] for i in range(max_count)]
