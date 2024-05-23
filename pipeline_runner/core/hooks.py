"""Hook manager for extensible lifecycle hooks."""

import logging
from typing import Any, Callable, Dict, List

logger = logging.getLogger(__name__)


class HookManager:
    """Manages named hooks that can be registered and triggered."""

    def __init__(self) -> None:
        self._hooks: Dict[str, List[Callable]] = {}

    def register_hook(self, name: str, callback: Callable) -> None:
        """Register a callback under the given hook name."""
        if name not in self._hooks:
            self._hooks[name] = []
        self._hooks[name].append(callback)
        logger.debug("Registered hook '%s' -> %s", name, callback.__name__)

    def trigger(self, name: str, *args: Any, **kwargs: Any) -> List[Any]:
        """Trigger all callbacks for the named hook and return results."""
        results: List[Any] = []
        for callback in self._hooks.get(name, []):
            try:
                results.append(callback(*args, **kwargs))
            except Exception:
                logger.exception(
                    "Error in hook '%s' callback %s", name, callback.__name__
                )
        return results

    def list_hooks(self) -> List[str]:
        """Return a list of registered hook names."""
        return list(self._hooks.keys())

    def has_hook(self, name: str) -> bool:
        """Check whether a hook has any registered callbacks."""
        return name in self._hooks and len(self._hooks[name]) > 0

    def cleanup(self, name: str) -> None:
        """Remove all callbacks for the given hook.

        Safe to call with unregistered names — silently does nothing.
        """
        # FIX: use pop with a default instead of del to avoid KeyError
        self._hooks.pop(name, None)
