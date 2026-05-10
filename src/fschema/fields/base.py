"""Base field types used by schemas."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from fschema.fs_interface import FSInterface


@dataclass(frozen=True)
class LoadContext:
    """Context passed to fields while loading a filesystem-like node."""

    path: Any
    fs: FSInterface
    load_schema: Callable[[Any, Any], Any]
    load_field: Callable[["Field", Any], Any]


class Field:
    """Base class for all fschema fields."""

    def __init__(self) -> None:
        self.attribute_name: str | None = None

    def bind(self, attribute_name: str) -> None:
        self.attribute_name = attribute_name

    def load(self, context: LoadContext) -> Any:
        raise NotImplementedError
