from video_notes.utils import clean_docx_text, fmt_time, safe_title


def test_fmt_time():
    assert fmt_time(0) == "00:00"
    assert fmt_time(65) == "01:05"
    assert fmt_time(3661) == "01:01:01"


def test_safe_title_removes_bad_filename_chars():
    assert safe_title('Bad:Title?/Video.mp4') == "Video"
    assert safe_title("Module_01-Intro.mp4") == "Module 01 Intro"


def test_clean_docx_text_normalizes_smart_punctuation():
    assert clean_docx_text('“Copywriting”—it’s useful…') == '"Copywriting"-it\'s useful...'
