# OpenCode / Generic Agent Instructions

When asked to create notes from a video, use the `video-notes` CLI.

Commands:

```bash
python -m pip install -e .
video-notes create "<VIDEO_OR_URL>" --out output --profile course --model-size small
video-notes qa "<PATH_TO_DOCX>"
```

Use `--download` only for internet videos the user has the right to access.

Default profiles:

- course: lessons and study material
- tutorial: demos and how-to videos
- meeting: meeting recordings
- interview: interviews and podcasts
- webinar: webinars and livestream replays
- general: anything else

Final answer should link the DOCX and mention QA results briefly.
