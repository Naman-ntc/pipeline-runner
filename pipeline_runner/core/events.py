"""Event bus for publish-subscribe messaging."""

import logging
from typing import Any, Callable, Dict, List

logger = logging.getLogger(__name__)


class EventBus:
    """Simple publish-subscribe event bus."""

    def __init__(self) -> None:
        self._subscribers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_name: str, callback: Callable) -> None:
        """Register a callback for the given event."""
        if event_name not in self._subscribers:
            self._subscribers[event_name] = []
        if callback in self._subscribers[event_name]:
            raise ValueError(
                f"Callback already subscribed to '{event_name}'"
            )
        self._subscribers[event_name].append(callback)

    def unsubscribe(self, event_name: str, callback: Callable) -> None:
        """Remove a callback from the given event."""
        # BUG: calls list.remove() without checking if callback is present,
        # raises ValueError when the callback was never subscribed.
        self._subscribers[event_name].remove(callback)

    def publish(self, event_name: str, *args: Any, **kwargs: Any) -> None:
        """Publish an event, invoking all registered callbacks."""
        for callback in self._subscribers.get(event_name, []):
            try:
                callback(*args, **kwargs)
            except Exception:
                logger.exception(
                    "Error in callback %s for event '%s'",
                    callback.__name__,
                    event_name,
                )

    def list_events(self) -> List[str]:
        """Return a list of events that have registered subscribers."""
        return list(self._subscribers.keys())

    def clear(self) -> None:
        """Remove all subscribers from every event."""
        self._subscribers.clear()
