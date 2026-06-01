# Roadmap

## Near Term

- Continue improving transcript-aware synthesis depth and profile-specific phrasing.
- Add scene-change screenshot selection.
- Add OCR/vision pass for slides and code.
- Add DOCX render QA through LibreOffice or Word automation.
- Add public sample video and sample DOCX.
- Expand generated video fixtures with audio and changing scenes.
- Version JSON artifact schemas for long-term agent compatibility.

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
