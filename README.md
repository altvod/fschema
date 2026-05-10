# fschema
Marshmallow-like schematization of a directory structure

## Quickstart Example

Let's say you have the following directory/file structure:
```
config/
  + plugins/
  |   + java/
  |   |   + plugin.yaml
  |   + python/
  |   |   + plugin.yaml
  + profiles/
  |   + new.yaml
  |   + old.yaml
  + env
  + config.yaml
```

You can describe it as a Python model and load everything into a single structure.

```python
from fschema.fields import meta, node
from fschema.schema import Schema
from fschema.fs_loader import FSLoader

class PluginConfigSchema(Schema):
    name = meta.NodeName()
    config = node.File(name="plugin.yaml")

class ProfileConfigSchema(Schema):
    name = meta.NodeName()
    config = meta.Content()

class ServiceConfigSchema(Schema):
    config = node.File(name="config.yaml")
    env = node.File(name="env")
    plugins = node.ListDirectory(node.SchematizedDirectory(PluginConfigSchema()))
    profiles = node.ListDirectory(node.SchematizedFile(PluginConfigSchema()))

data = FSLoader(schema=ServiceConfigSchema()).load("/path/to/config")
print(data)
```

This will load the following data:
```json
{
  "config": "<file-content>",
  "env": "<file-content>",
  "plugins": [
    {"name": "java", "config":  "<file-content>"},
    {"name": "python", "config":  "<file-content>"}
  ],
  "profiles": [
    {"name": "new.yaml", "config":  "<file-content>"},
    {"name": "old.yaml", "config":  "<file-content>"}
  ]
}
```

If you want to add post-processing of the data to your schema
(e.g. validate it or convert it to an object), you can define a `__fschema_post_load__` method:
```python
class ServiceConfigSchema(Schema):
    ...
    def __fschema_post_load__(self, data: dict) -> ServiceConfiguration:
        return ServiceConfiguration(**data)
```


## Reference

### Fields

#### Meta Fields

Meta fields are the fields that use the metadata of the respective filesystem node (directory/file)
and provide access to its various properties.

Meta field types:
- `NodeName()` - special type of field that loads the name of the current node (directory or file)
- `Content(reader: Reader, data_transformer: DataTransformer)` - for use inside a sub-schema of a `SchematizedFile`;
  `reader` parses the content to JSON-like data;
  `data_transformer` loads it into an object and/or validates the data

#### Node Fields

Node fields correspond to actual filesystem nodes (directories/fields).

All node fields have the optional argument `name` - this is the name of the filesystem node
the field corresponds to - useful if the filename has a period (`.`) in it,
and, therefore cannot be used as the field's attribute name.

Node field types:
- `SchematizedDirectory(directory_schema: Schema)` - load directory as a key-value mapping
  and apply the given sub-schema to the directory itself;
  this means nested files and directories must have fixed names
- `DictDirectory(nested_field: Field)` - load directory as a free mapping, without fixed key values;
  the given field instance is applied to all nested nodes
- `ListDirectory(nested_field: Field)` - load directory as a list of nodes;
  the given field instance is applied to all nested nodes
- `File(reader: Reader, data_transformer: DataTransformer)` - load file content;
  `reader` parses the content to JSON-like data;
  `data_transformer` loads it into an object and/or validates the data
- `SchematizedFile(file_schema: Schema)` - load the file as a schematized mapping instead of a single flat object;
  this is useful if you need access to its metadata (e.g. via `NodeName`);

### Content Readers

Available content readers:
- `JSONReader` - loads content as JSON (as a `dict`)
- `YamlReader` - loads data as YAML (as a `dict`)
- `TextReader` - loads data as text (`str`); this is the default reader

### Data Transformers

Available data transformers:
- `MarshmallowLoader(schema: marshmallow.Schema)` - loads the file data via a `marshmallow` schema
