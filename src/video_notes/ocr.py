from __future__ import annotations

from pathlib import Path
from typing import Any

from .artifacts import relative_path
from .exceptions import DependencyMissingError
from .utils import clean_docx_text


def extract_ocr_text(screenshots: list[Path], work_dir: Path) -> dict[str, Any]:
    try:
        import pytesseract  # type: ignore
    except ImportError as exc:
        raise DependencyMissingError("Install OCR support with: python -m pip install -e .[ocr]") from exc

    items = []
    for screenshot in screenshots:
        text = clean_docx_text(pytesseract.image_to_string(str(screenshot))).strip()
        if text:
            items.append(
                {
                    "screenshot": relative_path(screenshot, work_dir),
                    "text": text,
                }
            )
    return {
        "enabled": True,
        "engine": "pytesseract",
        "item_count": len(items),
        "items": items,
    }


def skipped_ocr_artifact() -> dict[str, Any]:
    return {
        "enabled": False,
        "engine": None,
        "item_count": 0,
        "items": [],
    }
