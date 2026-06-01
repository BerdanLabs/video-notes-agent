from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from .utils import find_libreoffice


def check_docx_render(path: Path, out_dir: Path | None = None) -> dict[str, Any]:
    libreoffice = find_libreoffice()
    if not libreoffice:
        return {
            "status": "skipped",
            "engine": None,
            "pdf": None,
            "problems": ["LibreOffice was not found; render QA was skipped."],
        }

    target_dir = out_dir or path.parent / "render_qa"
    target_dir.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        [
            libreoffice,
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            str(target_dir),
            str(path),
        ],
        capture_output=True,
        text=True,
    )
    pdf = target_dir / f"{path.stem}.pdf"
    problems = []
    if result.returncode != 0:
        problems.append(f"LibreOffice conversion failed: {result.stderr.strip() or result.stdout.strip()}")
    if not pdf.exists():
        problems.append("LibreOffice did not produce a PDF.")
    return {
        "status": "failed" if problems else "passed",
        "engine": "libreoffice",
        "pdf": str(pdf) if pdf.exists() else None,
        "problems": problems,
    }
