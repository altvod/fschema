"""Filesystem access interfaces."""

from fschema.fs.interface import FSInterface
from fschema.fs.local import LocalFSInterface

__all__ = ["FSInterface", "LocalFSInterface"]
