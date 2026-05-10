"""Base field types used by schemas."""

from __future__ import annotations

from copy import copy
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable

from fschema.fs import FSInterface

if TYPE_CHECKING:
    from fschema.schema import Schema


@dataclass(frozen=True)
class LoadContext:
    """Context passed to fields while loading a filesystem-like node."""

    path: Path
    fs: FSInterface
    load_schema: Callable[["Schema", Path], Any]
    load_field: Callable[["Field", Path], Any]


@dataclass(frozen=True)
class Field:
    """Base class for all fschema fields."""

    attribute_name: str | None = field(default=None, init=False)

    def bind(self, attribute_name: str) -> Field:
        bound = copy(self)
        object.__setattr__(bound, "attribute_name", attribute_name)
        return bound

    def load(self, context: LoadContext) -> Any:
        raise NotImplementedError
