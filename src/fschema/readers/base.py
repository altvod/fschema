"""Reader protocol."""

from __future__ import annotations

from typing import Any, Protocol


class Reader(Protocol):
    """Parse the content of a filesystem node."""

    def read(self, content: str) -> Any:
        """Return parsed content for raw file *content*."""
