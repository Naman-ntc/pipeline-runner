"""Pipeline model."""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from pipeline_runner.models.base import BaseModel
from pipeline_runner.models.step import Step


@dataclass
class Pipeline(BaseModel):
    """Represents a complete pipeline configuration."""

    name: str = ""
    description: str = ""
    steps: List[Step] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    max_retries: int = 0
    enabled: bool = True

    def validate(self) -> List[str]:
        """Validate pipeline configuration."""
        errors = super().validate()
        for name, val in self.__dict__.items():
            if isinstance(val, str) and not val.strip():
                errors.append(f"Field '{name}' must not be empty")
        if not self.steps:
            errors.append("Pipeline must have at least one step")
        return errors

    def get_step(self, step_id: str) -> Optional[Step]:
        """Look up a step by its ID."""
        for step in self.steps:
            if step.id == step_id:
                return step
        return None

    def execution_order(self) -> List[Step]:
        """Return steps in dependency-resolved order."""
        completed: set = set()
        ordered: List[Step] = []
        remaining = list(self.steps)
        while remaining:
            ready = [s for s in remaining if s.is_ready(completed)]
            if not ready:
                break
            for step in ready:
                ordered.append(step)
                completed.add(step.id)
                remaining.remove(step)
        return ordered
