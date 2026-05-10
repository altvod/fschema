"""Base field types used by schemas."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class LoadContext:
    """Filesystem node currently being loaded."""

    path: Path


class Field:
    """Base class for all fschema fields."""

    def __init__(self) -> None:
        self.attribute_name: str | None = None

    def bind(self, attribute_name: str) -> None:
        self.attribute_name = attribute_name

    def load(self, context: LoadContext) -> Any:
        raise NotImplementedError
