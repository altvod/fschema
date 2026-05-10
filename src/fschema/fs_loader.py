"""Filesystem loader entrypoint."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from fschema.fields.base import Field, LoadContext
from fschema.fs import FSInterface, LocalFSInterface


@dataclass(frozen=True)
class FSLoader:
    """Load a filesystem path with a schema."""

    schema: Any
    fs: FSInterface | None = field(default_factory=LocalFSInterface)

    def __post_init__(self) -> None:
        if self.fs is None:
            object.__setattr__(self, "fs", LocalFSInterface())

    def load(self, path: Any) -> Any:
        return self._load_schema(self.schema, path)

    def _load_schema(self, schema: Any, path: Any) -> Any:
        data = {
            attribute_name: self._load_field(field, path)
            for attribute_name, field in schema._declared_fields.items()
        }
        return schema.__fschema_post_load__(data)

    def _load_field(self, field: Field, path: Any) -> Any:
        context = LoadContext(
            path=path,
            fs=self.fs,
            load_schema=self._load_schema,
            load_field=self._load_field,
        )
        return field.load(context)
