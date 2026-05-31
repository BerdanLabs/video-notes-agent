from __future__ import annotations


PROFILES = {
    "course": ["Quick Summary", "Key Concepts", "Detailed Notes", "Practical Takeaways", "Review Questions"],
    "tutorial": ["Goal", "Steps", "Commands And Settings", "Gotchas", "Review Checklist"],
    "meeting": ["Summary", "Decisions", "Action Items", "Open Questions"],
    "interview": ["Summary", "Themes", "Notable Quotes", "Follow-Ups"],
    "webinar": ["Agenda", "Main Ideas", "Examples", "Q&A", "Next Steps"],
    "general": ["Summary", "Highlights", "Detailed Notes", "Takeaways"],
}


def get_profile(name: str) -> list[str]:
    return PROFILES.get(name, PROFILES["general"])
