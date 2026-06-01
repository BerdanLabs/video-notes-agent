# Agent Instructions

Use this project to create production-ready notes from videos.

Default workflow:

1. Resolve the source video.
   - Local file: use directly.
   - Internet URL: use `video-notes resolve` or `video-notes create --download` when legally accessible.
   - Never bypass DRM or unauthorized access controls.
2. Transcribe with local Whisper.
   - Use `small` for normal production notes.
   - Use `medium` for higher-stakes or noisy/Taglish videos when runtime is acceptable.
   - Use `tiny` only for smoke tests.
3. Extract/select screenshots.
   - Use screenshots as learning anchors, not decoration.
4. Create the DOCX.
   - Use natural, human study-note language.
   - Include short timestamped quotes.
   - Keep one DOCX per video.
5. Run QA.
   - Check `PHP`, `?s`, `?why`, `?poets?`, replacement characters, and internal test sections.
   - Print and review every paragraph containing `PHP` or `?`.
   - Structurally verify paragraphs, headings, tables, and embedded media.
6. Inspect JSON artifacts when debugging or chaining agents.
   - `artifacts/source.json` records the resolved source and profile.
   - `artifacts/transcript.json` records the transcript segments.
   - `artifacts/screenshots.json` records extracted and selected screenshots.
   - `artifacts/note_plan.json` records summary bullets, quotes, and planned sections.
   - `artifacts/outputs.json` records note output paths and QA reports.

Do not include internal implementation notes, model/runtime details, or comparison sections in final DOCX files unless the user explicitly asks for an audit.
