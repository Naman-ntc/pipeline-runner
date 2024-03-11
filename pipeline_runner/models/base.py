"""Base model with common fields and serialization."""
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List


@dataclass
class BaseModel:
    """Base model providing common fields and serialization."""

    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def to_dict(self) -> Dict[str, Any]:
        """Serialize model to dictionary."""
        raw = asdict(self)
        return {
            k: v.isoformat() if isinstance(v, datetime) else v
            for k, v in raw.items()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BaseModel":
        """Create model instance from dictionary."""
        field_names = {f.name for f in cls.__dataclass_fields__.values()}
        filtered = {k: v for k, v in data.items() if k in field_names}
        return cls(**filtered)

    def validate(self) -> List[str]:
        """Validate model fields. Returns list of error messages."""
        errors: List[str] = []
        for name, val in self.__dict__.items():
            if val is None:
                errors.append(f"Field '{name}' must not be None")
        return errors

    def touch(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = datetime.now(timezone.utc)
