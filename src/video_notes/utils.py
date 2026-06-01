from __future__ import annotations

import re
import shutil
from pathlib import Path


def find_ffmpeg() -> str | None:
    found = shutil.which("ffmpeg")
    if found:
        return found
    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return None


def find_libreoffice() -> str | None:
    for command in ("soffice", "libreoffice"):
        found = shutil.which(command)
        if found:
            return found
    return None


def safe_title(value: str, fallback: str = "Untitled Video") -> str:
    title = Path(value).stem if value else fallback
    title = re.sub(r"[_-]+", " ", title)
    title = re.sub(r"\s+", " ", title).strip()
    title = re.sub(r'[<>:"/\\|?*]', "", title)
    return title[:90] or fallback


def fmt_time(seconds: float) -> str:
    seconds = int(seconds)
    hh = seconds // 3600
    mm = (seconds % 3600) // 60
    ss = seconds % 60
    return f"{hh:02d}:{mm:02d}:{ss:02d}" if hh else f"{mm:02d}:{ss:02d}"


def clean_docx_text(text: str) -> str:
    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u2026": "...",
        "\u00a0": " ",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return re.sub(r"\s+", " ", text).strip()
