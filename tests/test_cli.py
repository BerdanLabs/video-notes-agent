from video_notes import cli
from video_notes.exceptions import SourceResolutionError


def test_cli_reports_video_notes_errors(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["video-notes", "create", "missing.mp4"])
    monkeypatch.setattr(
        cli,
        "run_create",
        lambda args: (_ for _ in ()).throw(SourceResolutionError("missing source")),
    )

    try:
        cli.main()
    except SystemExit as exc:
        assert exc.code == 1
    else:
        raise AssertionError("CLI should exit on VideoNotesError")

    assert "Error: missing source" in capsys.readouterr().err
