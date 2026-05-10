"""Schema definitions for fschema."""

from __future__ import annotations

from collections import OrderedDict
from dataclasses import dataclass
from typing import Any, ClassVar

from fschema.fields.base import Field


class SchemaMeta(type):
    """Collect field declarations from schema classes."""

    def __new__(mcls, name: str, bases: tuple[type, ...], namespace: dict[str, Any]):
        fields: OrderedDict[str, Field] = OrderedDict()
        for base in bases:
            fields.update(getattr(base, "_declared_fields", {}))

        for attribute_name, value in namespace.items():
            if isinstance(value, Field):
                bound_field = value.bind(attribute_name)
                namespace[attribute_name] = bound_field
                fields[attribute_name] = bound_field

        namespace["_declared_fields"] = fields
        return super().__new__(mcls, name, bases, namespace)


@dataclass(slots=True)
class Schema(metaclass=SchemaMeta):
    """Declarative schema for loading a filesystem node."""

    _declared_fields: ClassVar[OrderedDict[str, Field]]

    def __fschema_post_load__(self, data: dict[str, Any]) -> Any:
        return data
