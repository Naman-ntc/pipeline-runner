"""Run status tracking and run request model."""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
import uuid
from pipeline_runner.utils.helpers import sanitize_input


class RunStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class RunRequest:
    pipeline_name: str
    trigger: str
    parameters: dict = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: RunStatus = RunStatus.PENDING

    def __post_init__(self) -> None:
        self.pipeline_name = sanitize_input(self.pipeline_name)
        self.trigger = sanitize_input(self.trigger)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "pipeline_name": self.pipeline_name,
            "trigger": self.trigger,
            "parameters": self.parameters,
            "status": self.status.value,
        }

    def __repr__(self) -> str:
        return f"RunRequest(id={self.id!r}, pipeline={self.pipeline_name!r}, status={self.status.value!r})"
