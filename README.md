# Video Notes Agent

Local-first video note-taking engine for AI agents and humans.

It turns local or internet-accessible videos into polished study notes with:

- local Whisper transcription by default
- timestamped quotes
- selected screenshots
- DOCX output
- artifact checks for broken punctuation and transcript mistakes
- agent instructions for Codex, Claude Code, OpenCode, Antigravity-style tools, and other coding agents

## Status

Early open-source scaffold. The core package and CLI are being split out from a working Codex skill.

## Install

```bash
python -m pip install -e .
```

For internet video downloads:

```bash
python -m pip install -e ".[download]"
```

## Quick Start

Local video:

```bash
video-notes create "lesson.mp4" --out ./notes --profile course --model-size small
```

If `video-notes` is not on PATH, use:

```bash
python -m video_notes.cli create "lesson.mp4" --out ./notes --profile course --model-size small
```

Internet video:

```bash
video-notes create "https://www.youtube.com/watch?v=..." --out ./notes --profile tutorial --download
```

## Profiles

- `course`: study notes, key concepts, timestamped details, takeaways, review questions
- `tutorial`: goal, steps, commands, screenshots, gotchas
- `meeting`: summary, decisions, action items, open questions
- `interview`: themes, notable quotes, insights, follow-ups
- `webinar`: agenda, main ideas, examples, Q&A, next steps
- `general`: flexible notes for any video

## Privacy

The default transcription path is local open-source Whisper through `faster-whisper`.
No OpenAI API key is required for normal use.

## Copyright

Use this tool only with videos you have the right to access and process. Do not bypass DRM,
redistribute copyrighted course screenshots, or publish transcripts/notes where the source license
does not allow it.

## Agent Support

AI coding agents can use:

- `AGENTS.md` for universal instructions
- `adapters/codex/SKILL.md` for Codex
- `adapters/claude/VIDEO_NOTES.md` for Claude Code slash-command style usage
- the `video-notes` CLI for any agent that can run shell commands

Future work: MCP server adapter.

## Current Limitation

The initial CLI has the full pipeline shape, but rich note synthesis is still being moved from the
original agent workflow into reusable code. Today it creates a structured DOCX with transcript
quotes and screenshots; the roadmap tracks deeper profile-specific synthesis, OCR, scene-change
screenshot selection, and render QA.
