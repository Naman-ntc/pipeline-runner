"""Run status tracking for pipeline executions."""
from __future__ import annotations
from enum import Enum


class RunStatus(Enum):
    """Lifecycle states for a pipeline run."""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"
