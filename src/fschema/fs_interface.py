"""Filesystem access protocol and local filesystem implementation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
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


@dataclass(frozen=True)
class LocalFSInterface:
    """FSInterface implementation backed by pathlib and the local filesystem."""

    def node_name(self, path: str | Path) -> str:
        return Path(path).name

    def child_path(self, path: str | Path, fs_name: str) -> Path:
        return Path(path) / fs_name

    def list_directory(self, path: str | Path) -> list[Path]:
        return sorted(Path(path).iterdir(), key=lambda child: child.name)

    def require_file(self, path: str | Path) -> None:
        path = Path(path)
        if not path.is_file():
            raise FileNotFoundError(f"Expected file at {path}")

    def require_directory(self, path: str | Path) -> None:
        path = Path(path)
        if not path.is_dir():
            raise NotADirectoryError(f"Expected directory at {path}")

    def read_file(self, path: str | Path, *, encoding: str = "utf-8") -> str:
        return Path(path).read_text(encoding=encoding)
