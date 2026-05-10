"""Local filesystem implementation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class LocalFSInterface:
    """Filesystem interface implementation backed by pathlib."""

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
