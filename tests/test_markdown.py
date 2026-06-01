from pathlib import Path

from video_notes.markdown_writer import build_markdown


def test_build_markdown_generates_correct_file(tmp_path: Path):
    out_path = tmp_path / "notes.md"
    transcript = [
        {"start": 10, "text": "This is a key concept that we need to learn today."},
        {"start": 72, "text": "Another great tip for open-source development."},
    ]
    screenshots = [
        tmp_path / "00-10.png",
        tmp_path / "01-12.png",
    ]

    # Create dummy images so path calculations don't error out
    screenshots[0].touch()
    screenshots[1].touch()

    res_path = build_markdown(
        title="Intro to Testing",
        source="https://example.com/test",
        transcript=transcript,
        screenshots=screenshots,
        out_path=out_path,
        profile="tutorial",
    )

    assert res_path.exists()
    content = res_path.read_text(encoding="utf-8")

    # Assert correct structure
    assert "# Intro to Testing" in content
    assert "**Source:** https://example.com/test" in content
    assert "## Quick Summary" in content
    assert "## Memorable Lines" in content
    
    # Assert formatting of timestamps and quotes
    assert '> **00:10** - "This is a key concept that we need to learn today."' in content
    assert '> **01:12** - "Another great tip for open-source development."' in content

    # Assert screenshot rendering syntax (relative paths)
    assert "![Opening visual](00-10.png)" in content
    assert "![Selected frame: 01-12](01-12.png)" in content

    # Assert tutorial profile headers
    assert "### Steps" in content
    assert "### Commands" in content
