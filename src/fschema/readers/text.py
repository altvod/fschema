"""Text content reader."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class TextReader:
    """Return file content as text."""

    encoding: str = "utf-8"

    def read(self, content: str) -> str:
        return content
