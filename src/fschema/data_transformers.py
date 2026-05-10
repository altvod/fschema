"""Data transformers for parsed filesystem content."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


class DataTransformer(Protocol):
    """Transform parsed content into the final loaded value."""

    def transform(self, data: Any) -> Any:
        """Return transformed *data*."""


@dataclass(frozen=True)
class IdentityTransformer:
    """Return parsed content unchanged."""

    def transform(self, data: Any) -> Any:
        return data


@dataclass(frozen=True)
class MarshmallowLoader:
    """Load parsed data through a marshmallow schema."""

    schema: Any

    def transform(self, data: Any) -> Any:
        return self.schema.load(data)
