"""Marshmallow-like schematization of a directory structure."""

from fschema.fs import FSInterface, LocalFSInterface
from fschema.fs_loader import FSLoader
from fschema.schema import Schema

__version__ = "0.1.0"

__all__ = ["FSInterface", "FSLoader", "LocalFSInterface", "Schema", "__version__"]
