import json
from types import SimpleNamespace

import pytest

from video_notes import mcp_server


def test_create_notes_args_includes_optional_flags():
    args = mcp_server.create_notes_args(
        source="https://example.com/video",
        out="notes",
        profile="tutorial",
        model_size="medium",
        language="en",
        download=True,
        cookies="cookies.txt",
        screenshot_interval=10,
        max_screenshots=5,
        skip_transcript=True,
        skip_markdown=True,
        ocr=True,
        render_qa=True,
    )

    assert args == [
        "create",
        "https://example.com/video",
        "--out",
        "notes",
        "--profile",
        "tutorial",
        "--model-size",
        "medium",
        "--screenshot-interval",
        "10",
        "--max-screenshots",
        "5",
        "--language",
        "en",
        "--download",
        "--cookies",
        "cookies.txt",
        "--skip-transcript",
        "--skip-markdown",
        "--ocr",
        "--render-qa",
    ]


def test_qa_args_adds_render_flag():
    assert mcp_server.qa_args("notes.docx", render=True) == ["qa", "notes.docx", "--render"]


def test_run_cli_returns_json(monkeypatch):
    monkeypatch.setattr(
        mcp_server.subprocess,
        "run",
        lambda *args, **kwargs: SimpleNamespace(returncode=0, stdout='{"ok": true}', stderr=""),
    )

    assert mcp_server.run_cli(["qa", "notes.docx"]) == {"ok": True}


def test_run_cli_raises_on_cli_error(monkeypatch):
    monkeypatch.setattr(
        mcp_server.subprocess,
        "run",
        lambda *args, **kwargs: SimpleNamespace(returncode=1, stdout="", stderr="bad source"),
    )

    with pytest.raises(RuntimeError, match="bad source"):
        mcp_server.run_cli(["create", "missing.mp4"])


def test_read_artifact_tool_payload_shape(tmp_path):
    artifact = tmp_path / "artifact.json"
    artifact.write_text(json.dumps({"docx": "notes.docx"}), encoding="utf-8")

    assert json.loads(artifact.read_text(encoding="utf-8")) == {"docx": "notes.docx"}
