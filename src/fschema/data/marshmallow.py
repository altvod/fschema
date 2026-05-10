"""Marshmallow data transformer."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


class LoadSchema(Protocol):
    """Schema-like object with a marshmallow-compatible load method."""

    def load(self, data: Any) -> Any:
        """Load parsed *data*."""


@dataclass(frozen=True)
class MarshmallowLoader:
    """Load parsed data through a marshmallow schema."""

    schema: LoadSchema

    def transform(self, data: Any) -> Any:
        return self.schema.load(data)
