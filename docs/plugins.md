# Plugin system

Plugins extend the pipeline engine with custom steps without forking core code. The loader discovers entry points under the `pipeline.plugins` group and instantiates each class that subclasses `PluginBase`.

## PluginBase

`PluginBase` is an abstract base class. Subclasses must implement:

- `name` — unique string identifier used in YAML.
- `execute(context, config)` — returns a result object or raises `PluginError`.

Optional hooks include `validate_config(schema)` and `cleanup()` for long-lived resources.

## Writing a plugin

1. Subclass `PluginBase` and register the module via `pyproject.toml` entry points.
2. Declare a JSON Schema for your step’s `with:` block.
3. Use `context.workspace` for paths and `context.secrets` for injected credentials—never read arbitrary env vars directly in library code intended for reuse.

## Built-in plugins

- **Docker** — builds or runs images from a `Dockerfile` or image reference; supports build args and volume mounts under the workspace.
- **Shell** — runs a command in a subprocess with configurable cwd, timeout, and environment inheritance from the job context.

For examples, see `examples/plugins/` in the repository.
