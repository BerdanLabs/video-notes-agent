from __future__ import annotations

from pathlib import Path

from .profiles import get_profile
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
    
    # Title
    lines.append(f"# {title}")
    lines.append("")
    
    # Metadata
    lines.append(f"**Source:** {source}")
    lines.append("")
    
    # Quick Summary
    lines.append("## Quick Summary")
    lines.append("")
    for bullet in summarize_placeholder(transcript, profile):
        lines.append(f"- {bullet}")
    lines.append("")
    
    # Memorable Lines (Quotes)
    quote_candidates = transcript[:]
    lines.append("## Memorable Lines")
    lines.append("")
    for segment in select_quote_segments(quote_candidates):
        time_str = fmt_time(segment["start"])
        clean_text = clean_docx_text(segment["text"])
        lines.append(f'> **{time_str}** - "{clean_text}"')
        lines.append("")
    
    # Detailed Notes & Visual Anchors
    lines.append("## Detailed Notes")
    lines.append("")
    
    # Embedded first screenshot (opening visual)
    if screenshots:
        first_shot = screenshots[0]
        # Use relative path if possible, otherwise absolute
        try:
            rel_path = first_shot.relative_to(out_path.parent)
        except ValueError:
            rel_path = first_shot
        lines.append(f'![Opening visual]({rel_path.as_posix()})')
        lines.append("")
        lines.append("*Caption: Opening visual from the video.*")
        lines.append("")
        
    # Profile-specific sections
    for heading in get_profile(profile):
        if heading in {"Quick Summary", "Detailed Notes"}:
            continue
        lines.append(f"### {heading}")
        lines.append("")
        lines.append("Use the transcript and visuals to expand this section with human study notes.")
        lines.append("")
        
    # Remaining screenshots
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

    # Ensure parent directory exists
    out_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Save markdown file
    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path


def select_quote_segments(segments: list[dict], limit: int = 8) -> list[dict]:
    useful = [s for s in segments if 45 <= len(s.get("text", "")) <= 180]
    if len(useful) <= limit:
        return useful
    step = len(useful) / limit
    return [useful[int(i * step)] for i in range(limit)]


def summarize_placeholder(transcript: list[dict], profile: str) -> list[str]:
    if not transcript:
        return ["No transcript was available; expand notes from visual inspection."]
    return [
        f"This {profile} video was transcribed locally and organized into skimmable notes.",
        "Review the timestamped quotes and selected screenshots to revisit important moments.",
        "Expand each section with examples, definitions, warnings, and practical takeaways from the transcript.",
    ]
