"""Application configuration."""
from __future__ import annotations


def get_config() -> dict:
    return {
        "service_name": "pipeline-runner",
        "version": "0.1.0",
        "host": "0.0.0.0",
        "port": 8000,
        "debug": False,
    }
