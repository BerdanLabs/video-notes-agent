---
name: video-notes-agent
description: Create production-ready DOCX notes from local or internet videos using the video-notes-agent CLI. Use when the user wants notes, study guides, summaries, screenshots, timestamped quotes, transcripts, or review questions from course videos, tutorials, meetings, webinars, interviews, documentaries, or other videos.
---

# Video Notes Agent

Use the repository CLI rather than rewriting the workflow manually.

## Workflow

1. Install or use the package from the repo root:

```bash
python -m pip install -e .
```

2. Create notes:

```bash
video-notes create "path-or-url" --out output --profile course --model-size small
```

For URLs, add `--download` and ensure the user has legal access:

```bash
video-notes create "https://example.com/video" --download --out output --profile general
```

3. Run QA:

```bash
video-notes qa "output/Video Title/Video Title Notes.docx"
```

4. Deliver the final `.docx` only unless the user asks for transcripts or scratch files.

## Rules

- Use local Whisper by default.
- Use `small` for normal production notes and `medium` when quality matters more than runtime.
- Never bypass DRM or unauthorized access controls.
- Do not include internal test/comparison sections in the final DOCX unless requested.
- Fix QA problems before delivery.
