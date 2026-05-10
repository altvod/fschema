"""JSON content reader."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, kw_only=True)
class JSONReader:
    """Parse file content as JSON."""

    encoding: str = "utf-8"

    def read(self, content: str) -> Any:
        return json.loads(content)
