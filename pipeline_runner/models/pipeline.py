"""Pipeline model."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from pipeline_runner.models.base import BaseModel


@dataclass
class Pipeline(BaseModel):
    """Represents a pipeline definition."""

    name: str = ""
    steps: list[dict[str, Any]] = field(default_factory=list)
    owner: str = ""
    status: str = "draft"

    def add_step(self, step: dict[str, Any]) -> None:
        self.steps.append(step)

    def remove_step(self, index: int) -> None:
        del self.steps[index]

    def to_dict(self) -> dict[str, Any]:
        out = super().to_dict()
        out["step_count"] = len(self.steps)
        return out
