"""Shared pytest fixtures for pipeline-runner tests."""

import shutil
from pathlib import Path

import pytest


@pytest.fixture
def tmp_workspace(tmp_path):
    """Create an isolated workspace directory; removed with the session tmp_path."""
    workspace = tmp_path / "workspace"
    workspace.mkdir(parents=True, exist_ok=True)
    try:
        yield workspace
    finally:
        if workspace.exists():
            shutil.rmtree(workspace, ignore_errors=True)


@pytest.fixture
def sample_config():
    """Minimal configuration blob used across unit tests."""
    return {
        "service_name": "pipeline-runner",
        "environment": "test",
        "log_level": "INFO",
        "max_workers": 4,
        "timeout_seconds": 300,
    }


@pytest.fixture
def sample_pipeline():
    """Single-step pipeline definition for executor tests."""
    return {"name": "test", "steps": [{"id": "s1", "command": "echo ok"}]}


@pytest.fixture
def sample_step():
    """One build step with timeout metadata."""
    return {
        "id": "build",
        "name": "Build",
        "command": "make build",
        "timeout": 600,
    }
