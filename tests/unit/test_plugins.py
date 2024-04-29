"""Unit tests for the plugin loader and base plugin."""

import tempfile
import pytest
from pathlib import Path
from pipeline_runner.plugins.loader import PluginLoader
from pipeline_runner.plugins.base import PluginBase


def test_loader_discover_skips_init_files(tmp_path):
    (tmp_path / "__init__.py").write_text("# init")
    (tmp_path / "docker.py").write_text("x = 1")
    (tmp_path / "shell.py").write_text("y = 2")
    (tmp_path / "_internal.py").write_text("z = 3")
    loader = PluginLoader(str(tmp_path))
    found = loader.discover()
    assert "__init__" not in found
    assert "_internal" not in found
    assert "docker" in found
    assert "shell" in found


def test_loader_load_and_unload(tmp_path):
    (tmp_path / "sample.py").write_text("VALUE = 42")
    loader = PluginLoader(str(tmp_path))
    mod = loader.load("sample")
    assert mod.VALUE == 42
    assert "sample" in loader.list_plugins()
    assert loader.unload("sample") is True
    assert "sample" not in loader.list_plugins()
