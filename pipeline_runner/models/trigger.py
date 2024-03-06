"""Pipeline trigger model."""
import time
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class Trigger:
    """Represents an event that initiates a pipeline run."""

    source: str
    event_type: str
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    correlation_id: Optional[str] = None

    def matches(self, event_type: str, source: Optional[str] = None) -> bool:
        """Check if this trigger matches the given criteria."""
        if self.event_type != event_type:
            return False
        if source is not None and self.source != source:
            return False
        return True

    def age_seconds(self) -> float:
        """Return the age of this trigger in seconds."""
        return time.time() - self.timestamp

    def to_dict(self) -> Dict[str, Any]:
        """Serialize trigger to dictionary."""
        return {
            "source": self.source,
            "event_type": self.event_type,
            "payload": self.payload,
            "timestamp": self.timestamp,
            "correlation_id": self.correlation_id,
        }
