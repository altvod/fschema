"""Data transformers for parsed filesystem content."""

from __future__ import annotations

from typing import Any, Protocol


class DataTransformer(Protocol):
    """Transform parsed content into the final loaded value."""

    def transform(self, data: Any) -> Any:
        """Return transformed *data*."""


class IdentityTransformer:
    """Return parsed content unchanged."""

    def transform(self, data: Any) -> Any:
        return data


class MarshmallowLoader:
    """Load parsed data through a marshmallow schema."""

    def __init__(self, schema: Any) -> None:
        self.schema = schema

    def transform(self, data: Any) -> Any:
        return self.schema.load(data)
