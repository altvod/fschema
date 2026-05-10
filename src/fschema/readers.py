"""Content readers for filesystem-backed fields."""

from __future__ import annotations

import json
from typing import Any, Protocol


class Reader(Protocol):
    """Parse the content of a filesystem node."""

    def read(self, content: str) -> Any:
        """Return parsed content for raw file *content*."""


class TextReader:
    """Return file content as text."""

    def __init__(self, *, encoding: str = "utf-8") -> None:
        self.encoding = encoding

    def read(self, content: str) -> str:
        return content


class JSONReader:
    """Parse file content as JSON."""

    def __init__(self, *, encoding: str = "utf-8") -> None:
        self.encoding = encoding

    def read(self, content: str) -> Any:
        return json.loads(content)


class YamlReader:
    """Parse file content as YAML."""

    def __init__(self, *, encoding: str = "utf-8") -> None:
        self.encoding = encoding

    def read(self, content: str) -> Any:
        try:
            import yaml
        except ImportError as exc:
            raise RuntimeError("YamlReader requires PyYAML to be installed") from exc

        return yaml.safe_load(content)
