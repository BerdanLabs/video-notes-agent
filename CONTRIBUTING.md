# Contributing

Thanks for helping improve Video Notes Agent. The project is local-first, privacy-conscious, and intended to be useful from regular terminals and AI coding agents.

## Local Setup

```bash
python -m pip install -e ".[dev]"
```

For internet video support:

```bash
python -m pip install -e ".[download]"
```

Optional feature groups:

```bash
python -m pip install -e ".[ocr]"
python -m pip install -e ".[render]"
```

## Before Opening A PR

Run:

```bash
python -m pytest
```

If your change touches CLI help, generated files, or public docs, update the README or docs in the same PR.

## Contribution Areas

- note synthesis from transcripts
- screenshot selection and OCR
- DOCX and Markdown output quality
- QA validators
- internet video metadata and error handling
- agent adapters for Codex, Claude Code, OpenCode, and MCP
- tests with tiny synthetic fixtures

## Privacy And Copyright

Do not add features that bypass DRM, paywalls, or unauthorized access controls. URL support should help users process videos they have the right to access.

Avoid committing real course videos, private transcripts, private screenshots, or sample outputs from copyrighted material unless the source license clearly permits redistribution.

## Style

- Prefer small focused PRs.
- Add tests for behavior changes.
- Keep generated notes human-readable and skimmable.
- Keep dependencies optional when they are only needed for a specific feature.
