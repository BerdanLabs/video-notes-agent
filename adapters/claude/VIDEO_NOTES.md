# Video Notes Command

Use this as a Claude Code command/prompt template.

Task: Create production-ready DOCX notes from the provided video.

Steps:

1. Run `python -m pip install -e .` from the repo root if the CLI is not installed.
2. For local files:
   `video-notes create "<VIDEO>" --out output --profile course --model-size small`
3. For internet videos:
   `video-notes create "<URL>" --download --out output --profile general --model-size small`
4. Run:
   `video-notes qa "<DOCX>"`
5. If QA reports problems, fix the DOCX or rerun generation.
6. Return the final DOCX path.

Constraints:

- Local Whisper first.
- Do not bypass DRM or access controls.
- Do not publish copyrighted source material.
- Keep final notes human, skimmable, timestamped, and screenshot-supported.
