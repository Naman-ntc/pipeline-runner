"""Component registry for managing named objects."""

import threading
from typing import Any, Dict, List


class Registry:
    """Thread-safe registry for storing and retrieving named components."""

    def __init__(self) -> None:
        self._registry: Dict[str, Any] = {}
        self._lock = threading.Lock()

    def register(self, name: str, component: Any) -> None:
        """Register a component under the given name."""
        with self._lock:
            if name in self._registry:
                raise ValueError(
                    f"Component '{name}' is already registered"
                )
            self._registry[name] = component

    def get(self, name: str) -> Any:
        """Retrieve a component by name."""
        with self._lock:
            # BUG: returns None for missing names instead of raising KeyError
            return self._registry.get(name)

    def list_registered(self) -> List[str]:
        """Return a list of all registered component names."""
        with self._lock:
            return list(self._registry.keys())

    def has(self, name: str) -> bool:
        """Check whether a component is registered."""
        with self._lock:
            return name in self._registry

    def unregister(self, name: str) -> None:
        """Remove a component from the registry."""
        with self._lock:
            if name not in self._registry:
                raise KeyError(f"Component '{name}' is not registered")
            del self._registry[name]
