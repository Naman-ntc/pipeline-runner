"""Pipeline step model."""
from dataclasses import dataclass
from typing import List, Optional, Set


TERMINAL_STATUSES = frozenset({"succeeded", "failed", "skipped", "cancelled"})


@dataclass
class Step:
    """Represents a single step in a pipeline."""

    id: str
    name: str
    command: str
    timeout: int = 300
    depends_on: Optional[List[str]] = None
    status: str = "pending"

    def is_ready(self, completed_steps: Set[str]) -> bool:
        """Check whether all dependencies have completed."""
        if not self.depends_on:
            return True
        return all(dep in completed_steps for dep in self.depends_on)

    def is_terminal(self) -> bool:
        """Return True if step is in a terminal status."""
        return self.status in TERMINAL_STATUSES

    def start(self) -> None:
        """Mark step as running."""
        self.status = "running"

    def complete(self, success: bool = True) -> None:
        """Mark step as completed."""
        self.status = "succeeded" if success else "failed"

    def skip(self) -> None:
        """Mark step as skipped."""
        self.status = "skipped"
