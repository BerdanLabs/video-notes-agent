import pytest
from video_notes.exceptions import DependencyMissingError, VideoNotesError
from video_notes.resolver import resolve_source


def test_custom_exception_inheritance():
    exc = DependencyMissingError("test")
    assert isinstance(exc, VideoNotesError)
    assert isinstance(exc, Exception)


def test_resolve_source_raises_custom_exception(tmp_path):
    with pytest.raises(VideoNotesError) as exc_info:
        resolve_source("nonexistent.mp4", tmp_path)
    assert "Video file not found" in str(exc_info.value)
