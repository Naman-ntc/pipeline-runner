# Configuration

**pipeline-runner** uses a simple dict-based configuration loaded at startup. The canonical shape has five top-level keys used across core and API code.

## Fields

| Key            | Type   | Description                    |
|----------------|--------|--------------------------------|
| `service_name` | string | Logical name for this process  |
| `version`      | string | Release or build identifier    |
| `host`         | string | Bind address for the HTTP API  |
| `port`         | int    | Listen port                    |
| `debug`        | bool   | Enable verbose logging         |

## Loading config

Call `get_config()` to obtain the merged configuration (defaults plus overrides):

```python
from pipeline_runner.config import get_config

cfg = get_config()
print(cfg["host"], cfg["port"], cfg["debug"])
```

Override values by passing a dict to `get_config(overrides=...)` or by setting the documented environment variables before import, depending on your deployment.
