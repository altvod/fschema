"""Content readers for filesystem-backed fields."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Protocol


class Reader(Protocol):
    """Read and parse the content of a filesystem node."""

    def read(self, path: Path) -> Any:
        """Return parsed content for *path*."""


class TextReader:
    """Read file content as text."""

    def __init__(self, *, encoding: str = "utf-8") -> None:
        self.encoding = encoding

    def read(self, path: Path) -> str:
        return path.read_text(encoding=self.encoding)


class JSONReader:
    """Read file content as JSON."""

    def __init__(self, *, encoding: str = "utf-8") -> None:
        self.encoding = encoding

    def read(self, path: Path) -> Any:
        with path.open(encoding=self.encoding) as file:
            return json.load(file)


class YamlReader:
    """Read file content as YAML."""

    def __init__(self, *, encoding: str = "utf-8") -> None:
        self.encoding = encoding

    def read(self, path: Path) -> Any:
        try:
            import yaml
        except ImportError as exc:
            raise RuntimeError("YamlReader requires PyYAML to be installed") from exc

        with path.open(encoding=self.encoding) as file:
            return yaml.safe_load(file)
