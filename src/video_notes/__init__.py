"""Video Notes Agent."""

from .docx_writer import build_docx
from .markdown_writer import build_markdown

__version__ = "0.1.0"
__all__ = ["build_docx", "build_markdown"]
