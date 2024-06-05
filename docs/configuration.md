# Configuration

Load settings with the **`AppConfig`** dataclass and **`from_env()`** instead of untyped dicts.

```python
from dataclasses import dataclass
import os

@dataclass
class AppConfig:
    service_name: str
    version: str
    host: str
    port: int
    debug: bool

    @classmethod
    def from_env(cls) -> "AppConfig":
        return cls(
            service_name=os.environ.get("SERVICE_NAME", "pipeline-runner"),
            version=os.environ.get("VERSION", "0.0.0"),
            host=os.environ.get("HOST", "0.0.0.0"),
            port=int(os.environ.get("PORT", "8080")),
            debug=os.environ.get("DEBUG", "").lower() in ("1", "true", "yes"),
        )
```

**`SERVICE_NAME`** — logical service label. **`VERSION`** — release tag. **`HOST`** — bind address. **`PORT`** — listen port (must parse as int). **`DEBUG`** — truthy strings enable verbose diagnostics; invalid `PORT` should fail fast at startup.
