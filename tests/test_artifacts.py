from pathlib import Path

from video_notes.artifacts import (
    build_outputs_artifact,
    build_screenshot_artifact,
    relative_path,
    write_json_artifact,
)


def test_write_json_artifact_creates_parent_directory(tmp_path: Path):
    path = write_json_artifact(tmp_path / "artifacts" / "source.json", {"title": "Lesson"})

    assert path.exists()
    assert path.read_text(encoding="utf-8") == '{\n  "title": "Lesson"\n}'


def test_relative_path_prefers_work_dir_relative_paths(tmp_path: Path):
    work = tmp_path / "work"
    target = work / "frames" / "00-00-00.jpg"
    target.parent.mkdir(parents=True)
    target.touch()

    assert relative_path(target, work) == "frames/00-00-00.jpg"


def test_screenshot_artifact_records_selected_frames(tmp_path: Path):
    frames = [tmp_path / "frames" / f"{idx}.jpg" for idx in range(3)]
    for frame in frames:
        frame.parent.mkdir(parents=True, exist_ok=True)
        frame.touch()

    payload = build_screenshot_artifact(frames, [frames[0], frames[2]], tmp_path)

    assert payload["frame_count"] == 3
    assert payload["selected_count"] == 2
    assert payload["selected"] == ["frames/0.jpg", "frames/2.jpg"]


def test_outputs_artifact_includes_qa_reports(tmp_path: Path):
    docx = tmp_path / "Lesson Notes.docx"
    markdown = tmp_path / "Lesson Notes.md"

    payload = build_outputs_artifact(
        tmp_path,
        docx,
        {"problems": []},
        markdown,
        {"problems": ["missing screenshot"]},
    )

    assert payload["docx"]["path"] == "Lesson Notes.docx"
    assert payload["docx"]["qa"]["problems"] == []
    assert payload["markdown"]["path"] == "Lesson Notes.md"
    assert payload["markdown"]["qa"]["problems"] == ["missing screenshot"]
