"""Node fields that correspond to concrete filesystem children."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any

from fschema.data import DataTransformer, IdentityTransformer
from fschema.fields.base import Field, LoadContext
from fschema.readers import Reader, TextReader

if TYPE_CHECKING:
    from fschema.schema import Schema


@dataclass(frozen=True, kw_only=True)
class NodeField(Field):
    """Base class for fields that resolve filesystem child node names."""

    fs_name: str | None = None

    @property
    def effective_fs_name(self) -> str:
        """Filesystem node name resolved from ``fs_name`` or the schema attribute."""

        return self._resolve_fs_name()

    def _resolve_fs_name(self) -> str:
        if self.fs_name is not None:
            return self.fs_name
        if self.attribute_name is None:
            raise ValueError("Field is not bound to a schema attribute")
        return self.attribute_name

    def _resolve_path(self, context: LoadContext) -> Path:
        if self.fs_name is None and self.attribute_name is None:
            return context.path
        return context.fs.child_path(context.path, self._resolve_fs_name())


@dataclass(frozen=True, kw_only=True)
class File(NodeField):
    """Load a child file as parsed content."""

    reader: Reader | None = field(default_factory=TextReader)
    data_transformer: DataTransformer | None = field(
        default_factory=IdentityTransformer
    )

    def __post_init__(self) -> None:
        if self.reader is None:
            object.__setattr__(self, "reader", TextReader())
        if self.data_transformer is None:
            object.__setattr__(self, "data_transformer", IdentityTransformer())

    def load(self, context: LoadContext) -> Any:
        path = self._resolve_path(context)
        context.fs.require_file(path)
        encoding = getattr(self.reader, "encoding", "utf-8")
        content = context.fs.read_file(path, encoding=encoding)
        return self.data_transformer.transform(self.reader.read(content))


@dataclass(frozen=True, init=False)
class SchematizedFile(NodeField):
    """Load a child file through another schema."""

    file_schema: Schema

    def __init__(self, file_schema: Schema, *, fs_name: str | None = None) -> None:
        object.__setattr__(self, "attribute_name", None)
        object.__setattr__(self, "fs_name", fs_name)
        object.__setattr__(self, "file_schema", file_schema)

    def load(self, context: LoadContext) -> Any:
        path = self._resolve_path(context)
        context.fs.require_file(path)
        return context.load_schema(self.file_schema, path)


@dataclass(frozen=True, init=False)
class SchematizedDirectory(NodeField):
    """Load a child directory through another schema."""

    directory_schema: Schema

    def __init__(
        self,
        directory_schema: Schema,
        *,
        fs_name: str | None = None,
    ) -> None:
        object.__setattr__(self, "attribute_name", None)
        object.__setattr__(self, "fs_name", fs_name)
        object.__setattr__(self, "directory_schema", directory_schema)

    def load(self, context: LoadContext) -> Any:
        path = self._resolve_path(context)
        context.fs.require_directory(path)
        return context.load_schema(self.directory_schema, path)


@dataclass(frozen=True, init=False)
class DictDirectory(NodeField):
    """Load all children of a directory as a mapping."""

    nested_field: Field

    def __init__(self, nested_field: Field, *, fs_name: str | None = None) -> None:
        object.__setattr__(self, "attribute_name", None)
        object.__setattr__(self, "fs_name", fs_name)
        object.__setattr__(self, "nested_field", nested_field)

    def load(self, context: LoadContext) -> dict[str, Any]:
        path = self._resolve_path(context)
        context.fs.require_directory(path)
        return {
            context.fs.node_name(child): context.load_field(self.nested_field, child)
            for child in context.fs.list_directory(path)
        }


@dataclass(frozen=True, init=False)
class ListDirectory(NodeField):
    """Load all children of a directory as a list."""

    nested_field: Field

    def __init__(self, nested_field: Field, *, fs_name: str | None = None) -> None:
        object.__setattr__(self, "attribute_name", None)
        object.__setattr__(self, "fs_name", fs_name)
        object.__setattr__(self, "nested_field", nested_field)

    def load(self, context: LoadContext) -> list[Any]:
        path = self._resolve_path(context)
        context.fs.require_directory(path)
        return [
            context.load_field(self.nested_field, child)
            for child in context.fs.list_directory(path)
        ]
