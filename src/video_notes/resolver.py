from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from .exceptions import DependencyMissingError, SourceResolutionError
from .utils import safe_title


@dataclass
class Source:
    input: str
    path: Path
    title: str
    source_url: str | None = None
    retrieval_metadata: dict[str, Any] | None = None


def is_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"}


def resolve_source(value: str, out_dir: Path, download: bool = False) -> Source:
    if is_url(value):
        if not download:
            raise SourceResolutionError("URL input requires --download so access is explicit.")
        return download_url(value, out_dir)

    path = Path(value).expanduser().resolve()
    if not path.exists():
        raise SourceResolutionError(f"Video file not found: {path}")
    return Source(input=value, path=path, title=safe_title(path.name))


def download_url(url: str, out_dir: Path) -> Source:
    try:
        import yt_dlp  # type: ignore
    except ImportError as exc:
        raise DependencyMissingError(
            "Install URL support with: python -m pip install -e .[download]"
        ) from exc

    out_dir.mkdir(parents=True, exist_ok=True)
    template = str(out_dir / "%(title).180s.%(ext)s")
    opts = {
        "outtmpl": template,
        "format": "bv*+ba/best",
        "merge_output_format": "mp4",
        "quiet": True,
        "no_warnings": True,
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info.get("title") or safe_title(url)
        path = Path(ydl.prepare_filename(info))
        if path.suffix != ".mp4":
            merged = path.with_suffix(".mp4")
            if merged.exists():
                path = merged
    return Source(
        input=url,
        path=path.resolve(),
        title=safe_title(title),
        source_url=url,
        retrieval_metadata=extract_retrieval_metadata(info),
    )


def extract_retrieval_metadata(info: dict[str, Any]) -> dict[str, Any]:
    return {
        "extractor": info.get("extractor"),
        "extractor_key": info.get("extractor_key"),
        "id": info.get("id"),
        "webpage_url": info.get("webpage_url") or info.get("original_url"),
        "original_url": info.get("original_url"),
        "title": info.get("title"),
        "duration": info.get("duration"),
        "upload_date": info.get("upload_date"),
        "channel": info.get("channel") or info.get("uploader"),
        "channel_id": info.get("channel_id") or info.get("uploader_id"),
        "license": info.get("license"),
        "format_id": info.get("format_id"),
        "ext": info.get("ext"),
        "filesize_approx": info.get("filesize_approx"),
    }
