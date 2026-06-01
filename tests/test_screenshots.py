from pathlib import Path
from types import SimpleNamespace

from PIL import Image

from video_notes import screenshots


def test_select_representative_frames_keeps_short_lists(tmp_path: Path):
    frames = [tmp_path / f"{idx}.jpg" for idx in range(3)]

    assert screenshots.select_representative_frames(frames, max_count=5) == frames


def test_select_representative_frames_samples_evenly(tmp_path: Path):
    frames = [tmp_path / f"{idx}.jpg" for idx in range(10)]

    selected = screenshots.select_evenly_spaced_frames(frames, max_count=4)

    assert selected == [frames[0], frames[2], frames[5], frames[7]]


def test_select_representative_frames_prefers_scene_changes(tmp_path: Path):
    frames = []
    colors = ["navy", "navy", "white", "white", "black", "black"]
    for idx, color in enumerate(colors):
        frame = tmp_path / f"{idx}.jpg"
        Image.new("RGB", (32, 32), color=color).save(frame)
        frames.append(frame)

    selected = screenshots.select_representative_frames(frames, max_count=3)

    assert selected == [frames[0], frames[2], frames[4]]


def test_score_scene_changes_returns_empty_for_unreadable_frame(tmp_path: Path):
    bad = tmp_path / "bad.jpg"
    bad.write_text("not an image", encoding="utf-8")

    assert screenshots.score_scene_changes([bad]) == []


def test_probe_duration_parses_ffmpeg_stderr(monkeypatch, tmp_path: Path):
    def fake_run(*args, **kwargs):
        return SimpleNamespace(stderr="Duration: 00:01:02.50, start: 0.000000")

    monkeypatch.setattr(screenshots, "find_ffmpeg", lambda: "ffmpeg")
    monkeypatch.setattr(screenshots.subprocess, "run", fake_run)

    assert screenshots.probe_duration(tmp_path / "video.mp4") == 62.5
