"""Filesystem loader entrypoint."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any

from fschema.fields.base import Field, LoadContext
from fschema.fs import FSInterface, LocalFSInterface

if TYPE_CHECKING:
    from fschema.schema import Schema


@dataclass(frozen=True)
class FSLoader:
    """Load a filesystem path with a schema."""

    schema: Schema
    fs: FSInterface | None = field(default_factory=LocalFSInterface)

    def __post_init__(self) -> None:
        if self.fs is None:
            object.__setattr__(self, "fs", LocalFSInterface())

    def load(self, path: str | Path) -> Any:
        return self._load_schema(self.schema, Path(path))

    def _load_schema(self, schema: Schema, path: Path) -> Any:
        data = {
            attribute_name: self._load_field(field, path)
            for attribute_name, field in schema._declared_fields.items()
        }
        return schema.__fschema_post_load__(data)

    def _load_field(self, field: Field, path: Path) -> Any:
        context = LoadContext(
            path=path,
            fs=self.fs,
            load_schema=self._load_schema,
            load_field=self._load_field,
        )
        return field.load(context)
