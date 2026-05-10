"""Filesystem loader entrypoint."""

from __future__ import annotations

from pathlib import Path
from typing import Any


class FSLoader:
    """Load a filesystem path with a schema."""

    def __init__(self, schema: Any) -> None:
        self.schema = schema

    def load(self, path: str | Path) -> Any:
        return self.schema.load(Path(path))
