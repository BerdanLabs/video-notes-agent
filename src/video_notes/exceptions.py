from __future__ import annotations


class VideoNotesError(Exception):
    """Base exception for video-notes-agent."""


class DependencyMissingError(VideoNotesError):
    """A required external tool or dependency is missing."""


class SourceResolutionError(VideoNotesError):
    """Failed to resolve the video source URL or local path."""
