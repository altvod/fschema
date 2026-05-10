"""Meta fields that read properties of the current filesystem node."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from fschema.data_transformers import DataTransformer, IdentityTransformer
from fschema.fields.base import Field, LoadContext
from fschema.readers import Reader, TextReader


@dataclass(frozen=True)
class MetaField(Field):
    """Base class for fields that read the current filesystem node."""


@dataclass(frozen=True)
class NodeName(MetaField):
    """Load the name of the current filesystem node."""

    def load(self, context: LoadContext) -> str:
        return context.fs.node_name(context.path)


@dataclass(frozen=True)
class Content(MetaField):
    """Load the content of the current filesystem file."""

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
        context.fs.require_file(context.path)
        encoding = getattr(self.reader, "encoding", "utf-8")
        content = context.fs.read_file(context.path, encoding=encoding)
        return self.data_transformer.transform(self.reader.read(content))
