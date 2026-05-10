"""Meta fields that read properties of the current filesystem node."""

from __future__ import annotations

from fschema.data_transformers import DataTransformer, IdentityTransformer
from typing import Any

from fschema.fields.base import Field, LoadContext
from fschema.readers import Reader, TextReader


class MetaField(Field):
    """Base class for fields that read the current filesystem node."""


class NodeName(MetaField):
    """Load the name of the current filesystem node."""

    def load(self, context: LoadContext) -> str:
        return context.fs.node_name(context.path)


class Content(MetaField):
    """Load the content of the current filesystem file."""

    def __init__(
        self,
        reader: Reader | None = None,
        data_transformer: DataTransformer | None = None,
    ) -> None:
        super().__init__()
        self.reader = reader or TextReader()
        self.data_transformer = data_transformer or IdentityTransformer()

    def load(self, context: LoadContext) -> Any:
        context.fs.require_file(context.path)
        encoding = getattr(self.reader, "encoding", "utf-8")
        content = context.fs.read_file(context.path, encoding=encoding)
        return self.data_transformer.transform(self.reader.read(content))
