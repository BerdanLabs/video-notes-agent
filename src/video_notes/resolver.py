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


def resolve_source(
    value: str,
    out_dir: Path,
    download: bool = False,
    cookies: Path | None = None,
) -> Source:
    if is_url(value):
        if not download:
            raise SourceResolutionError("URL input requires --download so access is explicit.")
        return download_url(value, out_dir, cookies=cookies)

    path = Path(value).expanduser().resolve()
    if not path.exists():
        raise SourceResolutionError(f"Video file not found: {path}")
    return Source(input=value, path=path, title=safe_title(path.name))


def download_url(url: str, out_dir: Path, cookies: Path | None = None) -> Source:
    try:
        import yt_dlp  # type: ignore
    except ImportError as exc:
        raise DependencyMissingError(
            "Install URL support with: python -m pip install -e .[download]"
        ) from exc

    out_dir.mkdir(parents=True, exist_ok=True)
    opts = build_download_options(out_dir, cookies=cookies)
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get("title") or safe_title(url)
            path = Path(ydl.prepare_filename(info))
            if path.suffix != ".mp4":
                merged = path.with_suffix(".mp4")
                if merged.exists():
                    path = merged
    except Exception as exc:
        raise SourceResolutionError(classify_download_error(url, exc)) from exc
    return Source(
        input=url,
        path=path.resolve(),
        title=safe_title(title),
        source_url=url,
        retrieval_metadata=extract_retrieval_metadata(info),
    )


def build_download_options(out_dir: Path, cookies: Path | None = None) -> dict[str, Any]:
    opts: dict[str, Any] = {
        "outtmpl": str(out_dir / "%(title).180s.%(ext)s"),
        "format": "bv*+ba/best",
        "merge_output_format": "mp4",
        "quiet": True,
        "no_warnings": True,
    }
    if cookies:
        cookie_file = cookies.expanduser().resolve()
        if not cookie_file.exists():
            raise SourceResolutionError(f"Cookie file not found: {cookie_file}")
        opts["cookiefile"] = str(cookie_file)
    return opts


def classify_download_error(url: str, exc: Exception) -> str:
    detail = str(exc).strip()
    lowered = detail.lower()

    if any(term in lowered for term in ("drm", "encrypted", "protected content")):
        reason = "This video appears to be DRM-protected, so video-notes-agent will not try to bypass it."
    elif any(
        term in lowered
        for term in (
            "private",
            "sign in",
            "login",
            "forbidden",
            "unauthorized",
            "403",
            "cookies",
        )
    ):
        reason = (
            "This video is not accessible without authorization. Use only accounts and videos "
            "you have permission to process."
        )
    elif any(term in lowered for term in ("not available", "unavailable", "removed", "404")):
        reason = "This video is unavailable, removed, region-blocked, or the URL is incorrect."
    else:
        reason = "The video could not be downloaded."

    if detail:
        return f"{reason} Source: {url}. Downloader detail: {detail}"
    return f"{reason} Source: {url}."


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
