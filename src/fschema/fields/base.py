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

    def __init__(self, *, fs_name: str | None = None) -> None:
        self.fs_name = fs_name
        self.attribute_name: str | None = None

    def bind(self, attribute_name: str) -> None:
        self.attribute_name = attribute_name

    @property
    def effective_fs_name(self) -> str:
        """Filesystem node name resolved from ``fs_name`` or the schema attribute."""

        return self._resolve_fs_name()

    def _resolve_fs_name(self) -> str:
        if self.fs_name is not None:
            return self.fs_name
        if self.attribute_name is None:
            raise ValueError("Field is not bound to a schema attribute")
        return self.attribute_name

    def load(self, context: LoadContext) -> Any:
        raise NotImplementedError
