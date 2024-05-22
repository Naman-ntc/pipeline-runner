"""Pipeline trigger model."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional


@dataclass
class Trigger:
    """Represents an event that initiates a pipeline run."""

    source: str
    event_type: str
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
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
        delta = datetime.now(timezone.utc) - self.timestamp
        return delta.total_seconds()

    def to_dict(self) -> Dict[str, Any]:
        """Serialize trigger to dictionary."""
        return {
            "source": self.source,
            "event_type": self.event_type,
            "payload": self.payload,
            "timestamp": self.timestamp.isoformat(),
            "correlation_id": self.correlation_id,
        }
