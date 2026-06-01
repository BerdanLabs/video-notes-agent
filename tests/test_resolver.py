from pathlib import Path

import pytest

from video_notes.exceptions import SourceResolutionError
from video_notes.resolver import extract_retrieval_metadata, is_url, resolve_source


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


def test_extract_retrieval_metadata_keeps_auditable_fields():
    metadata = extract_retrieval_metadata(
        {
            "extractor": "youtube",
            "extractor_key": "Youtube",
            "id": "abc123",
            "webpage_url": "https://example.com/watch?v=abc123",
            "original_url": "https://short.example/abc123",
            "title": "A Helpful Lesson",
            "duration": 615,
            "upload_date": "20260531",
            "channel": "Berdan Labs",
            "channel_id": "channel-1",
            "license": "Creative Commons",
            "format_id": "137+140",
            "ext": "mp4",
            "filesize_approx": 123456,
            "formats": [{"url": "https://signed.example/video"}],
            "automatic_captions": {"en": []},
        }
    )

    assert metadata == {
        "extractor": "youtube",
        "extractor_key": "Youtube",
        "id": "abc123",
        "webpage_url": "https://example.com/watch?v=abc123",
        "original_url": "https://short.example/abc123",
        "title": "A Helpful Lesson",
        "duration": 615,
        "upload_date": "20260531",
        "channel": "Berdan Labs",
        "channel_id": "channel-1",
        "license": "Creative Commons",
        "format_id": "137+140",
        "ext": "mp4",
        "filesize_approx": 123456,
    }
    assert "formats" not in metadata
    assert "automatic_captions" not in metadata
