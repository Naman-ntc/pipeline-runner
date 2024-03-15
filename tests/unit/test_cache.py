"""Unit tests for CacheLayer."""

import time

from pipeline_runner.storage.cache import CacheLayer


class TestCacheLayer:
    def test_set_and_get(self):
        cache = CacheLayer(default_ttl_seconds=60)
        cache.set("k1", "value1")
        assert cache.get("k1") == "value1"

    def test_get_missing_returns_none(self):
        cache = CacheLayer()
        assert cache.get("nonexistent") is None

    def test_invalidate(self):
        cache = CacheLayer()
        cache.set("k1", 42)
        assert cache.invalidate("k1") is True
        assert cache.get("k1") is None
        assert cache.invalidate("k1") is False

    def test_ttl_expiry(self):
        cache = CacheLayer(default_ttl_seconds=0.05)
        cache.set("k1", "short-lived")
        time.sleep(0.06)
        assert cache.get("k1") is None

    def test_max_size_eviction(self):
        cache = CacheLayer(max_size=2, default_ttl_seconds=60)
        cache.set("a", 1)
        cache.set("b", 2)
        cache.set("c", 3)
        assert cache.size == 2
        assert cache.get("a") is None
