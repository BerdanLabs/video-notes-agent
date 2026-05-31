from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE

from .profiles import get_profile
from .utils import clean_docx_text, fmt_time


def build_docx(
    title: str,
    source: str,
    transcript: list[dict],
    screenshots: list[Path],
    out_path: Path,
    profile: str = "course",
) -> Path:
    doc = Document()
    setup_styles(doc)

    doc.add_paragraph(clean_docx_text(title), style="Title")
    meta = doc.add_paragraph()
    meta.add_run("Source: ").bold = True
    meta.add_run(clean_docx_text(source))

    doc.add_heading("Quick Summary", level=1)
    for bullet in summarize_placeholder(transcript, profile):
        doc.add_paragraph(clean_docx_text(bullet), style="List Bullet")

    quote_candidates = transcript[:]
    doc.add_heading("Memorable Lines", level=1)
    for segment in select_quote_segments(quote_candidates):
        p = doc.add_paragraph(style="Timestamp Quote")
        p.add_run(f'{fmt_time(segment["start"])} - "{clean_docx_text(segment["text"])}"')

    doc.add_heading("Detailed Notes", level=1)
    if screenshots:
        add_screenshot(doc, screenshots[0], "Opening visual from the video.")
    for heading in get_profile(profile):
        if heading in {"Quick Summary", "Detailed Notes"}:
            continue
        doc.add_heading(heading, level=2)
        doc.add_paragraph(
            clean_docx_text(
                "Use the transcript and visuals to expand this section with human study notes."
            )
        )

    if screenshots[1:]:
        doc.add_heading("Selected Screenshots", level=1)
        for shot in screenshots[1:]:
            add_screenshot(doc, shot, f"Selected frame: {shot.stem.replace('-', ':')}")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(out_path)
    return out_path


def setup_styles(doc: Document) -> None:
    styles = doc.styles
    styles["Normal"].font.name = "Aptos"
    styles["Normal"].font.size = Pt(10.5)
    for name, size, color in [
        ("Title", 23, "6F1026"),
        ("Heading 1", 16, "6F1026"),
        ("Heading 2", 13, "222222"),
    ]:
        style = styles[name]
        style.font.name = "Aptos"
        style.font.size = Pt(size)
        style.font.color.rgb = RGBColor.from_string(color)
        style.font.bold = True
    if "Timestamp Quote" not in styles:
        quote = styles.add_style("Timestamp Quote", WD_STYLE_TYPE.PARAGRAPH)
        quote.font.name = "Aptos"
        quote.font.size = Pt(9.5)
        quote.font.italic = True
        quote.font.color.rgb = RGBColor(65, 65, 65)


def add_screenshot(doc: Document, path: Path, caption: str) -> None:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture(str(path), width=Inches(6.25))
    cap = doc.add_paragraph(clean_docx_text(caption))
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER


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
