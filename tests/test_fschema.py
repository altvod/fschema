from __future__ import annotations

import json
import unittest
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from fschema.data_transformers import MarshmallowLoader
from fschema.fields import meta, node
from fschema.fs_loader import FSLoader
from fschema.readers import JSONReader
from fschema.schema import Schema


class FSchemaTests(unittest.TestCase):
    def test_loads_quickstart_style_directory_tree(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            _write(root / "config.yaml", "service: billing\n")
            _write(root / "env", "prod")
            _write(root / "plugins" / "java" / "plugin.yaml", "runtime: jvm")
            _write(root / "plugins" / "python" / "plugin.yaml", "runtime: cpython")
            _write(root / "profiles" / "new.yaml", "fresh")
            _write(root / "profiles" / "old.yaml", "legacy")

            class PluginConfigSchema(Schema):
                name = meta.NodeName()
                config = node.File(name="plugin.yaml")

            class ProfileConfigSchema(Schema):
                name = meta.NodeName()
                config = meta.Content()

            class ServiceConfigSchema(Schema):
                config = node.File(name="config.yaml")
                env = node.File(name="env")
                plugins = node.ListDirectory(
                    node.SchematizedDirectory(PluginConfigSchema())
                )
                profiles = node.ListDirectory(
                    node.SchematizedFile(ProfileConfigSchema())
                )

            self.assertEqual(
                FSLoader(schema=ServiceConfigSchema()).load(root),
                {
                    "config": "service: billing\n",
                    "env": "prod",
                    "plugins": [
                        {"name": "java", "config": "runtime: jvm"},
                        {"name": "python", "config": "runtime: cpython"},
                    ],
                    "profiles": [
                        {"name": "new.yaml", "config": "fresh"},
                        {"name": "old.yaml", "config": "legacy"},
                    ],
                },
            )

    def test_dict_directory_loads_children_by_name(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            _write(root / "profiles" / "new.txt", "fresh")
            _write(root / "profiles" / "old.txt", "legacy")

            class ProfilesSchema(Schema):
                profiles = node.DictDirectory(node.File())

            self.assertEqual(
                ProfilesSchema().load(root),
                {"profiles": {"new.txt": "fresh", "old.txt": "legacy"}},
            )

    def test_json_reader_and_data_transformer(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            _write(root / "settings.json", json.dumps({"enabled": True}))

            @dataclass
            class Settings:
                enabled: bool

            class SettingsLoader:
                def load(self, data: dict[str, Any]) -> Settings:
                    return Settings(**data)

            class ConfigSchema(Schema):
                settings = node.File(
                    name="settings.json",
                    reader=JSONReader(),
                    data_transformer=MarshmallowLoader(SettingsLoader()),
                )

            self.assertEqual(ConfigSchema().load(root), {"settings": Settings(True)})

    def test_schema_post_load_can_return_custom_object(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            _write(root / "env", "dev")

            @dataclass
            class Config:
                env: str

            class ConfigSchema(Schema):
                env = node.File()

                def __fschema_post_load__(self, data: dict[str, Any]) -> Config:
                    return Config(**data)

            self.assertEqual(ConfigSchema().load(root), Config(env="dev"))


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
