"""Data transformer protocol."""

from __future__ import annotations

from typing import Any, Protocol


class DataTransformer(Protocol):
    """Transform parsed content into the final loaded value."""

    def transform(self, data: Any) -> Any:
        """Return transformed *data*."""
