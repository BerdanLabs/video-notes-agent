import json
import subprocess
import sys
from pathlib import Path

import pytest

from video_notes.qa import check_notes
from video_notes.utils import find_ffmpeg


def test_cli_create_with_generated_video_fixture(tmp_path: Path):
    ffmpeg = find_ffmpeg()
    if not ffmpeg:
        pytest.skip("ffmpeg is required for the generated-video fixture")

    video = tmp_path / "fixture.mp4"
    subprocess.run(
        [
            ffmpeg,
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-f",
            "lavfi",
            "-i",
            "color=c=navy:s=320x180:d=2",
            "-pix_fmt",
            "yuv420p",
            str(video),
        ],
        check=True,
    )

    output_dir = tmp_path / "notes"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "video_notes",
            "create",
            str(video),
            "--out",
            str(output_dir),
            "--skip-transcript",
            "--screenshot-interval",
            "1",
            "--max-screenshots",
            "2",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    payload = json.loads(result.stdout)
    docx = Path(payload["docx"])
    markdown = Path(payload["markdown"])

    assert docx.exists()
    assert markdown.exists()
    assert payload["docx_qa"]["problems"] == []
    assert payload["markdown_qa"]["problems"] == []
    assert set(payload["artifacts"]) == {
        "source",
        "transcript",
        "screenshots",
        "ocr",
        "note_plan",
        "outputs",
    }

    work_dir = output_dir / "fixture"
    frames = sorted((work_dir / "frames").glob("*.jpg"))
    assert frames
    assert (work_dir / "frames.json").exists()
    for artifact in payload["artifacts"].values():
        assert (work_dir / artifact).exists()

    screenshots_artifact = json.loads((work_dir / payload["artifacts"]["screenshots"]).read_text())
    assert screenshots_artifact["frame_count"] >= 1
    assert screenshots_artifact["selected_count"] >= 1

    outputs_artifact = json.loads((work_dir / payload["artifacts"]["outputs"]).read_text())
    assert outputs_artifact["docx"]["qa"]["problems"] == []

    markdown_text = markdown.read_text(encoding="utf-8")
    assert "# fixture Notes" in markdown_text
    assert "No transcript was available" in markdown_text
    assert check_notes(docx)["images"] >= 1
    assert check_notes(markdown)["images"] >= 1
