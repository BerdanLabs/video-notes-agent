from pathlib import Path

import pytest

from video_notes.exceptions import SourceResolutionError
from video_notes.resolver import is_url, resolve_source


def test_is_url_accepts_http_and_https_only():
    assert is_url("https://example.com/video")
    assert is_url("http://example.com/video")
    assert not is_url("C:/videos/lesson.mp4")
    assert not is_url("ftp://example.com/video")


def test_resolve_source_local_file(tmp_path: Path):
    video = tmp_path / "Lesson One.mp4"
    video.write_bytes(b"placeholder")

    source = resolve_source(str(video), tmp_path)

    assert source.input == str(video)
    assert source.path == video.resolve()
    assert source.title == "Lesson One"
    assert source.source_url is None


def test_resolve_source_requires_explicit_download_for_urls(tmp_path: Path):
    with pytest.raises(SourceResolutionError, match="requires --download"):
        resolve_source("https://example.com/video", tmp_path)
