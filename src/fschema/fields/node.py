"""Node fields that correspond to concrete filesystem children."""

from __future__ import annotations

from pathlib import Path
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

    def _resolve_path(self, context: LoadContext) -> Path:
        if self.fs_name is None and self.attribute_name is None:
            return context.path
        return context.path / self._resolve_fs_name()


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
        path = _target_path(context, self)
        _require_file(path)
        return self.data_transformer.transform(self.reader.read(path))


class SchematizedFile(NodeField):
    """Load a child file through another schema."""

    def __init__(self, file_schema: Any, *, fs_name: str | None = None) -> None:
        super().__init__(fs_name=fs_name)
        self.file_schema = file_schema

    def load(self, context: LoadContext) -> Any:
        path = _target_path(context, self)
        _require_file(path)
        return self.file_schema.load(path)


class SchematizedDirectory(NodeField):
    """Load a child directory through another schema."""

    def __init__(self, directory_schema: SchematizedDirectory, *, fs_name: str | None = None) -> None:
        super().__init__(fs_name=fs_name)
        self.directory_schema = directory_schema

    def load(self, context: LoadContext) -> Any:
        path = _target_path(context, self)
        _require_directory(path)
        return self.directory_schema.load(path)


class DictDirectory(NodeField):
    """Load all children of a directory as a mapping."""

    def __init__(self, nested_field: Field, *, fs_name: str | None = None) -> None:
        super().__init__(fs_name=fs_name)
        self.nested_field = nested_field

    def load(self, context: LoadContext) -> dict[str, Any]:
        path = context.path / self.effective_fs_name
        _require_directory(path)
        return {
            child.name: self.nested_field.load(LoadContext(child))
            for child in _iter_children(path)
        }


class ListDirectory(NodeField):
    """Load all children of a directory as a list."""

    def __init__(self, nested_field: Field, *, fs_name: str | None = None) -> None:
        super().__init__(fs_name=fs_name)
        self.nested_field = nested_field

    def load(self, context: LoadContext) -> list[Any]:
        path = context.path / self.effective_fs_name
        _require_directory(path)
        return [self.nested_field.load(LoadContext(child)) for child in _iter_children(path)]


def _iter_children(path: Path) -> list[Path]:
    return sorted(path.iterdir(), key=lambda child: child.name)


def _target_path(context: LoadContext, field: NodeField) -> Path:
    return field._resolve_path(context)


def _require_file(path: Path) -> None:
    if not path.is_file():
        raise FileNotFoundError(f"Expected file at {path}")


def _require_directory(path: Path) -> None:
    if not path.is_dir():
        raise NotADirectoryError(f"Expected directory at {path}")
