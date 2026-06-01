# Roadmap

## Near Term

- Continue improving transcript-aware synthesis depth and profile-specific phrasing.
- Add configurable scene-change thresholds and screenshot captions.
- Integrate OCR text into DOCX and Markdown synthesis.
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
- Add browser cookie import helpers for user-authorized sessions.
- Expand retrieval metadata with schema versioning and optional provenance checks.
- Expand DRM/access-control refusal tests with real extractor error fixtures.
