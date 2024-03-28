"""Metrics collection with thread-safe counters, gauges, and histograms."""

import threading
from typing import Any, Dict, List, Optional


class MetricsCollector:
    """Collects and manages application metrics in a thread-safe manner."""

    def __init__(self) -> None:
        self._metrics: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()

    def counter(self, name: str, value: float = 1.0) -> None:
        """Increment a counter metric by the given value."""
        with self._lock:
            if name not in self._metrics:
                self._metrics[name] = {"type": "counter", "value": 0.0}
            self._metrics[name]["value"] += value

    def gauge(self, name: str, value: float) -> None:
        """Set a gauge metric to the given value."""
        with self._lock:
            self._metrics[name] = {"type": "gauge", "value": value}

    def histogram(self, name: str, value: float) -> None:
        """Record a value in a histogram metric."""
        with self._lock:
            if name not in self._metrics:
                self._metrics[name] = {
                    "type": "histogram",
                    "values": [],
                    "count": 0,
                    "sum": 0.0,
                }
            self._metrics[name]["values"].append(value)
            self._metrics[name]["count"] += 1
            self._metrics[name]["sum"] += value

    def get(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a single metric by name, or None if it does not exist."""
        with self._lock:
            metric = self._metrics.get(name)
            if metric is None:
                return None
            return dict(metric)

    def export(self) -> Dict[str, Dict[str, Any]]:
        """Export all collected metrics."""
        with self._lock:
            # BUG: returns the internal dict directly — callers can mutate it
            return self._metrics

    def reset(self) -> None:
        """Clear all collected metrics."""
        with self._lock:
            self._metrics.clear()
