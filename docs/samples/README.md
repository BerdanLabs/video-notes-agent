# Public Samples

These files are synthetic and safe to redistribute. The sample video is generated from plain color
frames, not from a private course, meeting, or copyrighted lesson.

Included files:

- `sample-video.mp4`: tiny generated video fixture.
- `generated/sample video/sample video Notes.docx`: sample DOCX output.
- `generated/sample video/sample video Notes.md`: sample Markdown output.
- `generated/sample video/artifacts/*.json`: machine-readable source, transcript, screenshot, OCR,
  note-plan, and QA artifacts.

Regenerate the sample locally:

```bash
video-notes create docs/samples/sample-video.mp4 --out docs/samples/generated --skip-transcript --screenshot-interval 1 --max-screenshots 3
```

The sample intentionally skips transcription because the fixture has no audio. Real lecture or course
videos should use local Whisper transcription unless you pass `--skip-transcript` for a quick smoke
test.
