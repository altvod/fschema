"""Content readers for filesystem-backed fields."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Protocol


class Reader(Protocol):
    """Parse the content of a filesystem node."""

    def read(self, content: str) -> Any:
        """Return parsed content for raw file *content*."""


@dataclass(frozen=True, kw_only=True)
class TextReader:
    """Return file content as text."""

    encoding: str = "utf-8"

    def read(self, content: str) -> str:
        return content


@dataclass(frozen=True, kw_only=True)
class JSONReader:
    """Parse file content as JSON."""

    encoding: str = "utf-8"

    def read(self, content: str) -> Any:
        return json.loads(content)


@dataclass(frozen=True, kw_only=True)
class YamlReader:
    """Parse file content as YAML."""

    encoding: str = "utf-8"

    def read(self, content: str) -> Any:
        try:
            import yaml
        except ImportError as exc:
            raise RuntimeError("YamlReader requires PyYAML to be installed") from exc

        return yaml.safe_load(content)
