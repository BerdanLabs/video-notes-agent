from pathlib import Path
from types import SimpleNamespace

import pytest

from video_notes import ocr
from video_notes.exceptions import DependencyMissingError


def test_skipped_ocr_artifact():
    assert ocr.skipped_ocr_artifact() == {
        "enabled": False,
        "engine": None,
        "item_count": 0,
        "items": [],
    }


def test_extract_ocr_text_records_non_empty_text(monkeypatch, tmp_path: Path):
    screenshot = tmp_path / "frames" / "00-00-00.jpg"
    screenshot.parent.mkdir()
    screenshot.touch()

    monkeypatch.setitem(
        __import__("sys").modules,
        "pytesseract",
        SimpleNamespace(image_to_string=lambda path: "Slide title\nImportant code example"),
    )

    payload = ocr.extract_ocr_text([screenshot], tmp_path)

    assert payload["enabled"] is True
    assert payload["engine"] == "pytesseract"
    assert payload["item_count"] == 1
    assert payload["items"] == [
        {
            "screenshot": "frames/00-00-00.jpg",
            "text": "Slide title Important code example",
        }
    ]


def test_extract_ocr_text_requires_optional_dependency(monkeypatch, tmp_path: Path):
    monkeypatch.delitem(__import__("sys").modules, "pytesseract", raising=False)

    real_import = __import__

    def fake_import(name, *args, **kwargs):
        if name == "pytesseract":
            raise ImportError("missing")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr("builtins.__import__", fake_import)

    with pytest.raises(DependencyMissingError, match="Install OCR support"):
        ocr.extract_ocr_text([], tmp_path)
