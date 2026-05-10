"""YAML content reader."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, kw_only=True)
class YamlReader:
    """Parse file content as YAML."""

    encoding: str = "utf-8"

    def read(self, content: str) -> Any:
        try:
            import yaml
        except ImportError as exc:
            raise RuntimeError("YamlReader requires PyYAML to be installed") from exc

        return yaml.safe_load(content)
