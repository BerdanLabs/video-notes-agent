from __future__ import annotations

from pathlib import Path

from .synthesis import build_note_plan
from .utils import clean_docx_text, fmt_time


def build_markdown(
    title: str,
    source: str,
    transcript: list[dict],
    screenshots: list[Path],
    out_path: Path,
    profile: str = "course",
) -> Path:
    """Build a beautifully formatted Markdown notes file."""
    lines = []
    note_plan = build_note_plan(transcript, profile)

    lines.append(f"# {title}")
    lines.append("")

    lines.append(f"**Source:** {source}")
    lines.append("")

    lines.append("## Quick Summary")
    lines.append("")
    for bullet in note_plan["summary"]:
        lines.append(f"- {bullet}")
    lines.append("")

    lines.append("## Memorable Lines")
    lines.append("")
    for segment in note_plan["quotes"]:
        time_str = fmt_time(segment["start"])
        clean_text = clean_docx_text(segment["text"])
        lines.append(f'> **{time_str}** - "{clean_text}"')
        lines.append("")

    lines.append("## Detailed Notes")
    lines.append("")

    if screenshots:
        first_shot = screenshots[0]
        try:
            rel_path = first_shot.relative_to(out_path.parent)
        except ValueError:
            rel_path = first_shot
        lines.append(f'![Opening visual]({rel_path.as_posix()})')
        lines.append("")
        lines.append("*Caption: Opening visual from the video.*")
        lines.append("")

    for heading, bullets in note_plan["sections"].items():
        lines.append(f"### {heading}")
        lines.append("")
        for bullet in bullets:
            lines.append(f"- {bullet}")
        lines.append("")

    if screenshots[1:]:
        lines.append("## Selected Screenshots")
        lines.append("")
        for shot in screenshots[1:]:
            try:
                rel_path = shot.relative_to(out_path.parent)
            except ValueError:
                rel_path = shot
            lines.append(f'![Selected frame: {shot.stem}]({rel_path.as_posix()})')
            lines.append("")
            lines.append(f"*Caption: Selected frame at {shot.stem.replace('-', ':')}*")
            lines.append("")

    out_path.parent.mkdir(parents=True, exist_ok=True)

    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path


def summarize_placeholder(transcript: list[dict], profile: str) -> list[str]:
    return build_note_plan(transcript, profile)["summary"]
