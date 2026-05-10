"""Schema definitions for fschema."""

from __future__ import annotations

from collections import OrderedDict
from pathlib import Path
from typing import Any

from fschema.fields.base import Field, LoadContext


class SchemaMeta(type):
    """Collect field declarations from schema classes."""

    def __new__(mcls, name: str, bases: tuple[type, ...], namespace: dict[str, Any]):
        fields: OrderedDict[str, Field] = OrderedDict()
        for base in bases:
            fields.update(getattr(base, "_declared_fields", {}))

        for attribute_name, value in namespace.items():
            if isinstance(value, Field):
                value.bind(attribute_name)
                fields[attribute_name] = value

        namespace["_declared_fields"] = fields
        return super().__new__(mcls, name, bases, namespace)


class Schema(metaclass=SchemaMeta):
    """Declarative schema for loading a filesystem node."""

    _declared_fields: OrderedDict[str, Field]

    def load(self, path: str | Path) -> Any:
        context = LoadContext(Path(path))
        data = {
            attribute_name: field.load(context)
            for attribute_name, field in self._declared_fields.items()
        }
        return self.__fschema_post_load__(data)

    def __fschema_post_load__(self, data: dict[str, Any]) -> Any:
        return data
