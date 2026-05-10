"""Identity data transformer."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class IdentityTransformer:
    """Return parsed content unchanged."""

    def transform(self, data: Any) -> Any:
        return data
