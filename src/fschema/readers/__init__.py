"""Content readers for filesystem-backed fields."""

from fschema.readers.base import Reader
from fschema.readers.json import JSONReader
from fschema.readers.text import TextReader
from fschema.readers.yaml import YamlReader

__all__ = ["JSONReader", "Reader", "TextReader", "YamlReader"]
