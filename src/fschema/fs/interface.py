"""Filesystem access protocol."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol


class FSInterface(Protocol):
    """Filesystem-like operations needed by fschema fields."""

    def node_name(self, path: Path) -> str:
        """Return the display name of *path*."""

    def child_path(self, path: Path, fs_name: str) -> Path:
        """Return the child path named *fs_name* under *path*."""

    def list_directory(self, path: Path) -> list[Path]:
        """Return children of the directory at *path*."""

    def require_file(self, path: Path) -> None:
        """Raise if *path* is not a file."""

    def require_directory(self, path: Path) -> None:
        """Raise if *path* is not a directory."""

    def read_file(self, path: Path, *, encoding: str = "utf-8") -> str:
        """Return file content from *path*."""
