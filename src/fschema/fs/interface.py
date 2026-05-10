"""Filesystem access protocol."""

from __future__ import annotations

from typing import Any, Protocol


class FSInterface(Protocol):
    """Filesystem-like operations needed by fschema fields."""

    def node_name(self, path: Any) -> str:
        """Return the display name of *path*."""

    def child_path(self, path: Any, fs_name: str) -> Any:
        """Return the child path named *fs_name* under *path*."""

    def list_directory(self, path: Any) -> list[Any]:
        """Return children of the directory at *path*."""

    def require_file(self, path: Any) -> None:
        """Raise if *path* is not a file."""

    def require_directory(self, path: Any) -> None:
        """Raise if *path* is not a directory."""

    def read_file(self, path: Any, *, encoding: str = "utf-8") -> str:
        """Return file content from *path*."""
