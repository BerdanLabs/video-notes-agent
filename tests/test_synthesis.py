from video_notes.synthesis import build_note_plan, extract_keywords, select_quote_segments


TRANSCRIPT = [
    {
        "start": 0,
        "end": 8,
        "text": "Today we define the testing strategy for video notes and explain why fixtures matter.",
    },
    {
        "start": 12,
        "end": 24,
        "text": "A generated fixture keeps the pipeline repeatable without downloading course videos.",
    },
    {
        "start": 30,
        "end": 45,
        "text": "The final review checklist should confirm Markdown, DOCX, screenshots, and QA output.",
    },
]


def test_build_note_plan_uses_transcript_content():
    plan = build_note_plan(TRANSCRIPT, "course")

    assert "testing" in " ".join(plan["summary"])
    assert "Key Concepts" in plan["sections"]
    assert "Review Questions" in plan["sections"]
    assert any("00:00" in bullet for bullet in plan["sections"]["Key Concepts"])
    assert plan["quotes"]


def test_build_note_plan_handles_missing_transcript():
    plan = build_note_plan([], "tutorial")

    assert plan["summary"] == ["No transcript was available; expand notes from visual inspection."]
    assert plan["quotes"] == []
    assert "Steps" in plan["sections"]


def test_extract_keywords_ignores_common_words():
    keywords = extract_keywords(TRANSCRIPT)

    assert "testing" in keywords
    assert "video" in keywords
    assert "that" not in keywords


def test_select_quote_segments_limits_long_lists():
    segments = [{"start": idx, "text": f"This is a useful transcript sentence number {idx}."} for idx in range(20)]

    assert len(select_quote_segments(segments, limit=5)) == 5
