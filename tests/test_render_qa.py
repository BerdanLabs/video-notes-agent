from pathlib import Path
from types import SimpleNamespace

from video_notes import render_qa


def test_check_docx_render_skips_without_libreoffice(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(render_qa, "find_libreoffice", lambda: None)

    report = render_qa.check_docx_render(tmp_path / "notes.docx")

    assert report["status"] == "skipped"
    assert report["engine"] is None
    assert report["problems"]


def test_check_docx_render_passes_when_pdf_is_created(monkeypatch, tmp_path: Path):
    docx = tmp_path / "notes.docx"
    docx.touch()

    def fake_run(args, **kwargs):
        out_dir = Path(args[args.index("--outdir") + 1])
        (out_dir / "notes.pdf").write_bytes(b"%PDF")
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    monkeypatch.setattr(render_qa, "find_libreoffice", lambda: "soffice")
    monkeypatch.setattr(render_qa.subprocess, "run", fake_run)

    report = render_qa.check_docx_render(docx, tmp_path / "rendered")

    assert report["status"] == "passed"
    assert report["engine"] == "libreoffice"
    assert report["pdf"].endswith("notes.pdf")
    assert report["problems"] == []


def test_check_docx_render_reports_conversion_failure(monkeypatch, tmp_path: Path):
    docx = tmp_path / "notes.docx"
    docx.touch()

    monkeypatch.setattr(render_qa, "find_libreoffice", lambda: "soffice")
    monkeypatch.setattr(
        render_qa.subprocess,
        "run",
        lambda *args, **kwargs: SimpleNamespace(returncode=1, stdout="", stderr="bad file"),
    )

    report = render_qa.check_docx_render(docx, tmp_path / "rendered")

    assert report["status"] == "failed"
    assert any("bad file" in problem for problem in report["problems"])
    assert any("did not produce" in problem for problem in report["problems"])
