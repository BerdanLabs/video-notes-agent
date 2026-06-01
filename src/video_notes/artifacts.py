from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .resolver import Source


def write_json_artifact(path: Path, payload: dict[str, Any] | list[Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def relative_path(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def build_source_artifact(source: Source, work_dir: Path, profile: str) -> dict[str, Any]:
    return {
        "input": source.input,
        "title": source.title,
        "profile": profile,
        "source_url": source.source_url,
        "resolved_path": relative_path(source.path, work_dir),
    }


def build_screenshot_artifact(
    frames: list[Path],
    selected: list[Path],
    work_dir: Path,
) -> dict[str, Any]:
    return {
        "frame_count": len(frames),
        "selected_count": len(selected),
        "frames": [relative_path(path, work_dir) for path in frames],
        "selected": [relative_path(path, work_dir) for path in selected],
    }


def build_outputs_artifact(
    work_dir: Path,
    docx: Path,
    docx_report: dict[str, Any],
    markdown: Path | None = None,
    markdown_report: dict[str, Any] | None = None,
) -> dict[str, Any]:
    outputs: dict[str, Any] = {
        "docx": {
            "path": relative_path(docx, work_dir),
            "qa": docx_report,
        }
    }
    if markdown and markdown_report:
        outputs["markdown"] = {
            "path": relative_path(markdown, work_dir),
            "qa": markdown_report,
        }
    return outputs
