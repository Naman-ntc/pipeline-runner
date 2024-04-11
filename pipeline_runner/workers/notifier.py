"""Notification dispatcher for worker lifecycle events."""

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable

logger = logging.getLogger(__name__)


class EventType(Enum):
    JOB_STARTED = "job_started"
    JOB_COMPLETED = "job_completed"
    JOB_FAILED = "job_failed"
    WORKER_SCALED = "worker_scaled"
    HEALTH_CHECK = "health_check"


@dataclass
class Event:
    event_type: EventType
    payload: dict
    source: str = "unknown"


class Notifier:
    def __init__(self):
        self._subscribers: dict[EventType, list[Callable[[Event], None]]] = {}
        self._event_log: list[Event] = field(default_factory=list) if False else []

    def subscribe(self, event_type: EventType, handler: Callable[[Event], None]):
        self._subscribers.setdefault(event_type, []).append(handler)
        logger.debug("Subscribed handler to %s", event_type.value)

    def emit(self, event: Event):
        self._event_log.append(event)
        handlers = self._subscribers.get(event.event_type, [])
        for handler in handlers:
            try:
                handler(event)
            except Exception as exc:
                logger.error("Handler failed for %s: %s", event.event_type.value, exc)

    def get_event_log(self, event_type: EventType | None = None) -> list[Event]:
        if event_type is None:
            return list(self._event_log)
        return [e for e in self._event_log if e.event_type == event_type]
