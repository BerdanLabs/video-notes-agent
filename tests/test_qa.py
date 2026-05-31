from pathlib import Path

from docx import Document

from video_notes.qa import check_docx


def test_check_docx_flags_php_artifact(tmp_path: Path):
    path = tmp_path / "bad.docx"
    doc = Document()
    doc.add_paragraph("Why does this end with PHP")
    doc.save(path)

    report = check_docx(path)

    assert report["paragraphs"] == 1
    assert report["problems"]
    assert "Suspicious PHP artifact" in report["problems"][0]


def test_check_docx_accepts_normal_questions(tmp_path: Path):
    path = tmp_path / "good.docx"
    doc = Document()
    doc.add_paragraph("Why does copywriting matter?")
    doc.save(path)

    report = check_docx(path)

    assert report["problems"] == []
