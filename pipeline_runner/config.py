"""Application configuration."""
from __future__ import annotations
import os
from dataclasses import dataclass


@dataclass
class AppConfig:
    service_name: str = "pipeline-runner"
    version: str = "0.1.0"
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False

    @classmethod
    def from_env(cls) -> "AppConfig":
        return cls(
            service_name=os.environ.get("SERVICE_NAME", "pipeline-runner"),
            version=os.environ.get("VERSION", "0.1.0"),
            host=os.environ.get("HOST", "0.0.0.0"),
            port=int(os.environ.get("PORT", "8000")),
            debug=os.environ.get("DEBUG", "").lower() in ("1", "true", "yes"),
        )


def get_config() -> AppConfig:
    """Load configuration from environment."""
    return AppConfig.from_env()
