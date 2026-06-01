from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any


def run_cli(args: list[str]) -> dict[str, Any]:
    result = subprocess.run(
        [sys.executable, "-m", "video_notes", *args],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(detail or f"video-notes exited with code {result.returncode}")
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"video-notes returned non-JSON output: {result.stdout[:500]}") from exc


def create_notes_args(
    source: str,
    out: str = "output",
    profile: str = "course",
    model_size: str = "small",
    language: str | None = None,
    download: bool = False,
    cookies: str | None = None,
    screenshot_interval: int = 30,
    max_screenshots: int = 12,
    skip_transcript: bool = False,
    skip_markdown: bool = False,
    ocr: bool = False,
    render_qa: bool = False,
) -> list[str]:
    args = [
        "create",
        source,
        "--out",
        out,
        "--profile",
        profile,
        "--model-size",
        model_size,
        "--screenshot-interval",
        str(screenshot_interval),
        "--max-screenshots",
        str(max_screenshots),
    ]
    if language:
        args.extend(["--language", language])
    if download:
        args.append("--download")
    if cookies:
        args.extend(["--cookies", cookies])
    if skip_transcript:
        args.append("--skip-transcript")
    if skip_markdown:
        args.append("--skip-markdown")
    if ocr:
        args.append("--ocr")
    if render_qa:
        args.append("--render-qa")
    return args


def qa_args(notes_file: str, render: bool = False) -> list[str]:
    args = ["qa", notes_file]
    if render:
        args.append("--render")
    return args


def build_server():
    try:
        from mcp.server.fastmcp import FastMCP  # type: ignore
    except ImportError as exc:
        raise RuntimeError("Install MCP support with: python -m pip install -e .[mcp]") from exc

    server = FastMCP("video-notes-agent")

    @server.tool()
    def create_docx_notes(
        source: str,
        out: str = "output",
        profile: str = "course",
        model_size: str = "small",
        language: str | None = None,
        download: bool = False,
        cookies: str | None = None,
        screenshot_interval: int = 30,
        max_screenshots: int = 12,
        skip_transcript: bool = False,
        skip_markdown: bool = False,
        ocr: bool = False,
        render_qa: bool = False,
    ) -> dict[str, Any]:
        """Create DOCX notes and JSON artifacts from a local or authorized internet video."""
        return run_cli(
            create_notes_args(
                source=source,
                out=out,
                profile=profile,
                model_size=model_size,
                language=language,
                download=download,
                cookies=cookies,
                screenshot_interval=screenshot_interval,
                max_screenshots=max_screenshots,
                skip_transcript=skip_transcript,
                skip_markdown=skip_markdown,
                ocr=ocr,
                render_qa=render_qa,
            )
        )

    @server.tool()
    def qa_notes(notes_file: str, render: bool = False) -> dict[str, Any]:
        """QA a generated DOCX or Markdown notes file."""
        return run_cli(qa_args(notes_file, render=render))

    @server.tool()
    def read_artifact(path: str) -> dict[str, Any]:
        """Read a JSON artifact emitted by video-notes-agent."""
        return json.loads(Path(path).read_text(encoding="utf-8"))

    return server


def main() -> None:
    build_server().run()


if __name__ == "__main__":
    main()
