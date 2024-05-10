"""In-memory cache layer with TTL support."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class _CacheEntry:
    value: Any
    created_at: float
    ttl: Optional[float]


class CacheLayer:
    """Simple in-memory cache with per-key TTL and max-size eviction."""

    def __init__(self, max_size: int = 1024, default_ttl_seconds: float = 300) -> None:
        self.max_size = max_size
        self.default_ttl_seconds = default_ttl_seconds
        self._store: dict[str, _CacheEntry] = {}

    def _is_expired(self, entry: _CacheEntry) -> bool:
        if entry.ttl is None:
            return False
        elapsed = time.monotonic() - entry.created_at
        if elapsed >= entry.ttl:
            return True
        return False

    def _evict_oldest(self) -> None:
        if not self._store:
            return
        oldest_key = next(iter(self._store))
        del self._store[oldest_key]

    def get(self, key: str) -> Optional[Any]:
        entry = self._store.get(key)
        if entry is None:
            return None
        if self._is_expired(entry):
            del self._store[key]
            return None
        return entry.value

    def set(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        if ttl is None:
            ttl = self.default_ttl_seconds
        while len(self._store) >= self.max_size and key not in self._store:
            self._evict_oldest()
        self._store[key] = _CacheEntry(
            value=value,
            created_at=time.monotonic(),
            ttl=ttl,
        )

    def invalidate(self, key: str) -> bool:
        """Remove *key* from cache. Returns True if it was present."""
        return self._store.pop(key, None) is not None

    def clear(self) -> None:
        self._store.clear()

    @property
    def size(self) -> int:
        return len(self._store)
