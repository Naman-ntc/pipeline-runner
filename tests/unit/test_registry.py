"""Tests for the Registry component."""

import pytest

from pipeline_runner.core.registry import Registry


class TestRegistry:
    def test_register_and_get(self):
        r = Registry()
        r.register("comp", {"key": "value"})
        assert r.get("comp") == {"key": "value"}

    def test_get_missing_raises(self):
        r = Registry()
        with pytest.raises(KeyError):
            r.get("nonexistent")

    def test_register_duplicate_raises(self):
        r = Registry()
        r.register("comp", 1)
        with pytest.raises(ValueError):
            r.register("comp", 2)

    def test_has(self):
        r = Registry()
        assert not r.has("comp")
        r.register("comp", 1)
        assert r.has("comp")

    def test_list_registered(self):
        r = Registry()
        r.register("a", 1)
        r.register("b", 2)
        assert sorted(r.list_registered()) == ["a", "b"]
