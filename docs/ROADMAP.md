# Roadmap

## Near Term

- Replace placeholder note synthesis with a richer transcript-aware synthesis engine.
- Add scene-change screenshot selection.
- Add OCR/vision pass for slides and code.
- Add DOCX render QA through LibreOffice or Word automation.
- Add public sample video and sample DOCX.
- Add tests with a tiny generated video fixture.

## Agent Interop

- Add MCP server exposing:
  - `resolve_video`
  - `transcribe_video`
  - `extract_screenshots`
  - `create_docx_notes`
  - `qa_docx`
- Add packaged Codex skill export.
- Add Claude Code slash command installer.

## Internet Video Support

- Harden `yt-dlp` URL resolution.
- Add cookie-file option for user-authorized sessions.
- Store retrieval metadata.
- Add clear DRM/access-control refusal messages.
