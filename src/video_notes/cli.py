from __future__ import annotations

import argparse
import json
from pathlib import Path

from .exceptions import VideoNotesError
from .docx_writer import build_docx
from .markdown_writer import build_markdown
from .qa import check_notes
from .resolver import resolve_source
from .screenshots import extract_frames, select_representative_frames
from .transcribe import transcribe_local
from .utils import safe_title


def main() -> None:
    parser = argparse.ArgumentParser(prog="video-notes")
    sub = parser.add_subparsers(dest="command", required=True)

    create = sub.add_parser("create", help="Create notes from a video")
    create.add_argument("source")
    create.add_argument("--out", type=Path, default=Path("output"))
    create.add_argument("--profile", default="course")
    create.add_argument("--model-size", default="small")
    create.add_argument("--language")
    create.add_argument("--download", action="store_true")
    create.add_argument("--screenshot-interval", type=int, default=30)
    create.add_argument("--max-screenshots", type=int, default=12)
    create.add_argument("--skip-transcript", action="store_true")
    create.add_argument("--skip-markdown", action="store_true", help="Skip Markdown notes generation")

    qa = sub.add_parser("qa", help="Check a generated DOCX or Markdown file")
    qa.add_argument("notes_file", type=Path, help="Path to the generated .docx or .md file")

    args = parser.parse_args()
    try:
        if args.command == "create":
            run_create(args)
        elif args.command == "qa":
            print(json.dumps(check_notes(args.notes_file), indent=2))
    except VideoNotesError as exc:
        parser.exit(1, f"Error: {exc}\n")


def run_create(args: argparse.Namespace) -> None:
    source_tmp = args.out / "_sources"
    source = resolve_source(args.source, source_tmp, download=args.download)
    title = safe_title(source.title)
    work = args.out / title
    work.mkdir(parents=True, exist_ok=True)

    transcript = []
    if not args.skip_transcript:
        transcript = transcribe_local(
            source.path,
            work / "transcript",
            model_size=args.model_size,
            language=args.language,
        )

    frames = extract_frames(source.path, work, interval=args.screenshot_interval)
    shots = select_representative_frames(frames, max_count=args.max_screenshots)
    
    docx = build_docx(
        title=f"{title} Notes",
        source=source.source_url or str(source.path),
        transcript=transcript,
        screenshots=shots,
        out_path=work / f"{title} Notes.docx",
        profile=args.profile,
    )
    
    md_path = None
    if not args.skip_markdown:
        md_path = build_markdown(
            title=f"{title} Notes",
            source=source.source_url or str(source.path),
            transcript=transcript,
            screenshots=shots,
            out_path=work / f"{title} Notes.md",
            profile=args.profile,
        )
        
    docx_report = check_notes(docx)
    result = {
        "docx": str(docx),
        "docx_qa": docx_report
    }
    
    if md_path:
        md_report = check_notes(md_path)
        result["markdown"] = str(md_path)
        result["markdown_qa"] = md_report
        
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
