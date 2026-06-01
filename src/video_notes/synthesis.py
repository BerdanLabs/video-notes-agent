from __future__ import annotations

import re
from collections import Counter

from .profiles import get_profile
from .utils import clean_docx_text, fmt_time


STOPWORDS = {
    "about",
    "after",
    "again",
    "also",
    "because",
    "before",
    "being",
    "could",
    "every",
    "from",
    "have",
    "into",
    "just",
    "like",
    "more",
    "much",
    "need",
    "only",
    "other",
    "should",
    "that",
    "their",
    "then",
    "there",
    "these",
    "they",
    "this",
    "through",
    "what",
    "when",
    "where",
    "which",
    "with",
    "would",
    "your",
}


def build_note_plan(transcript: list[dict], profile: str) -> dict:
    """Create deterministic, transcript-grounded notes for all output writers."""
    segments = normalize_segments(transcript)
    if not segments:
        return {
            "summary": ["No transcript was available; expand notes from visual inspection."],
            "quotes": [],
            "sections": {
                heading: ["Use the transcript and visuals to expand this section with human study notes."]
                for heading in get_profile(profile)
                if heading not in {"Quick Summary", "Detailed Notes", "Summary"}
            },
        }

    keywords = extract_keywords(segments)
    return {
        "summary": summarize_segments(segments, profile, keywords),
        "quotes": select_quote_segments(segments),
        "sections": build_sections(segments, profile, keywords),
    }


def normalize_segments(transcript: list[dict]) -> list[dict]:
    normalized = []
    for item in transcript:
        text = clean_docx_text(str(item.get("text", "")))
        if not text:
            continue
        normalized.append(
            {
                "start": float(item.get("start", 0) or 0),
                "end": float(item.get("end", item.get("start", 0)) or 0),
                "text": text,
            }
        )
    return normalized


def summarize_segments(segments: list[dict], profile: str, keywords: list[str]) -> list[str]:
    duration = max(segment.get("end", 0) or segment["start"] for segment in segments)
    opening = segments[0]["text"]
    close = segments[-1]["text"]
    bullets = [
        f"This {profile} video runs about {fmt_time(duration)} and opens with: {trim_sentence(opening)}",
        f"The clearest recurring topics are {', '.join(keywords[:5])}."
        if keywords
        else "The transcript is short, so the notes focus on the visible sequence of ideas.",
    ]
    if close != opening:
        bullets.append(f"It closes around {fmt_time(segments[-1]['start'])} with: {trim_sentence(close)}")
    return bullets


def build_sections(segments: list[dict], profile: str, keywords: list[str]) -> dict[str, list[str]]:
    section_names = [
        heading
        for heading in get_profile(profile)
        if heading not in {"Quick Summary", "Detailed Notes", "Summary"}
    ]
    if not section_names:
        section_names = ["Highlights", "Takeaways"]

    chunks = split_evenly(segments, len(section_names))
    sections: dict[str, list[str]] = {}
    for heading, chunk in zip(section_names, chunks):
        sections[heading] = section_bullets(heading, chunk, keywords)
    return sections


def section_bullets(heading: str, segments: list[dict], keywords: list[str]) -> list[str]:
    if not segments:
        return ["No transcript detail was available for this section."]
    first = segments[0]
    bullets = [f"{fmt_time(first['start'])}: {trim_sentence(first['text'])}"]
    if len(segments) > 1:
        last = segments[-1]
        bullets.append(f"{fmt_time(last['start'])}: {trim_sentence(last['text'])}")
    if heading.lower() in {"key concepts", "themes", "main ideas", "highlights"} and keywords:
        bullets.append(f"Terms to revisit: {', '.join(keywords[:6])}.")
    if heading.lower() in {"review questions", "review checklist"}:
        bullets.append(f"Can you explain why this moment matters: {trim_sentence(first['text'])}")
    if heading.lower() in {"practical takeaways", "takeaways", "follow-ups", "action items"}:
        bullets.append("Convert this section into concrete next actions after reviewing the source video.")
    return bullets


def select_quote_segments(segments: list[dict], limit: int = 8) -> list[dict]:
    useful = [s for s in segments if 35 <= len(s.get("text", "")) <= 220]
    if len(useful) <= limit:
        return useful
    step = len(useful) / limit
    return [useful[int(i * step)] for i in range(limit)]


def extract_keywords(segments: list[dict], limit: int = 8) -> list[str]:
    words = re.findall(r"[A-Za-z][A-Za-z'-]{3,}", " ".join(s["text"] for s in segments).lower())
    counts = Counter(word for word in words if word not in STOPWORDS)
    return [word for word, _count in counts.most_common(limit)]


def split_evenly(items: list[dict], groups: int) -> list[list[dict]]:
    if groups <= 0:
        return []
    size = max(len(items) / groups, 1)
    chunks = []
    for index in range(groups):
        start = int(index * size)
        end = int((index + 1) * size)
        chunks.append(items[start:end] or items[-1:])
    return chunks


def trim_sentence(text: str, limit: int = 180) -> str:
    text = clean_docx_text(text)
    if len(text) <= limit:
        return text
    return text[: limit - 3].rsplit(" ", 1)[0] + "..."
