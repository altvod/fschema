"""Node fields that correspond to concrete filesystem children."""

from __future__ import annotations

from typing import Any

from fschema.data_transformers import DataTransformer, IdentityTransformer
from fschema.fields.base import Field, LoadContext
from fschema.readers import Reader, TextReader


class NodeField(Field):
    """Base class for fields that resolve filesystem child node names."""

    def __init__(self, *, fs_name: str | None = None) -> None:
        super().__init__()
        self.fs_name = fs_name

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

    def _resolve_path(self, context: LoadContext) -> Any:
        if self.fs_name is None and self.attribute_name is None:
            return context.path
        return context.fs.child_path(context.path, self._resolve_fs_name())


class File(NodeField):
    """Load a child file as parsed content."""

    def __init__(
        self,
        *,
        fs_name: str | None = None,
        reader: Reader | None = None,
        data_transformer: DataTransformer | None = None,
    ) -> None:
        super().__init__(fs_name=fs_name)
        self.reader = reader or TextReader()
        self.data_transformer = data_transformer or IdentityTransformer()

    def load(self, context: LoadContext) -> Any:
        path = self._resolve_path(context)
        context.fs.require_file(path)
        encoding = getattr(self.reader, "encoding", "utf-8")
        content = context.fs.read_file(path, encoding=encoding)
        return self.data_transformer.transform(self.reader.read(content))


class SchematizedFile(NodeField):
    """Load a child file through another schema."""

    def __init__(self, file_schema: Any, *, fs_name: str | None = None) -> None:
        super().__init__(fs_name=fs_name)
        self.file_schema = file_schema

    def load(self, context: LoadContext) -> Any:
        path = self._resolve_path(context)
        context.fs.require_file(path)
        return context.load_schema(self.file_schema, path)


class SchematizedDirectory(NodeField):
    """Load a child directory through another schema."""

    def __init__(self, directory_schema: Any, *, fs_name: str | None = None) -> None:
        super().__init__(fs_name=fs_name)
        self.directory_schema = directory_schema

    def load(self, context: LoadContext) -> Any:
        path = self._resolve_path(context)
        context.fs.require_directory(path)
        return context.load_schema(self.directory_schema, path)


class DictDirectory(NodeField):
    """Load all children of a directory as a mapping."""

    def __init__(self, nested_field: Field, *, fs_name: str | None = None) -> None:
        super().__init__(fs_name=fs_name)
        self.nested_field = nested_field

    def load(self, context: LoadContext) -> dict[str, Any]:
        path = self._resolve_path(context)
        context.fs.require_directory(path)
        return {
            context.fs.node_name(child): context.load_field(self.nested_field, child)
            for child in context.fs.list_directory(path)
        }


class ListDirectory(NodeField):
    """Load all children of a directory as a list."""

    def __init__(self, nested_field: Field, *, fs_name: str | None = None) -> None:
        super().__init__(fs_name=fs_name)
        self.nested_field = nested_field

    def load(self, context: LoadContext) -> list[Any]:
        path = self._resolve_path(context)
        context.fs.require_directory(path)
        return [
            context.load_field(self.nested_field, child)
            for child in context.fs.list_directory(path)
        ]
