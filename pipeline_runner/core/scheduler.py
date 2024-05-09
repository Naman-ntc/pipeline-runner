"""Job scheduler with time-based triggering."""

import logging
import time
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List

logger = logging.getLogger(__name__)


class Scheduler:
    """Simple time-based job scheduler."""

    def __init__(self) -> None:
        self._jobs: Dict[str, Dict[str, Any]] = {}

    def schedule(
        self,
        job_id: str,
        callback: Callable,
        interval_seconds: float,
        immediate: bool = False,
    ) -> None:
        """Schedule a job to run at the given interval."""
        if job_id in self._jobs:
            raise ValueError(f"Job '{job_id}' already scheduled")
        now = time.monotonic()
        self._jobs[job_id] = {
            "callback": callback,
            "interval": interval_seconds,
            "next_run": now if immediate else now + interval_seconds,
            "last_run": None,
            "run_count": 0,
            # FIX: use timezone-aware UTC instead of deprecated utcnow()
            "created_at": datetime.now(timezone.utc),
        }

    def unschedule(self, job_id: str) -> None:
        """Remove a scheduled job."""
        if job_id not in self._jobs:
            raise KeyError(f"Job '{job_id}' not found")
        del self._jobs[job_id]

    def tick(self) -> List[str]:
        """Check and execute any jobs that are due. Returns executed job ids."""
        now = time.monotonic()
        executed: List[str] = []
        for job_id, job in list(self._jobs.items()):
            if now >= job["next_run"]:
                try:
                    job["callback"]()
                    job["last_run"] = now
                    job["run_count"] += 1
                    job["next_run"] = now + job["interval"]
                    executed.append(job_id)
                except Exception:
                    logger.exception("Job '%s' failed during tick", job_id)
        return executed

    def list_jobs(self) -> List[str]:
        """Return all scheduled job ids."""
        return list(self._jobs.keys())

    def get_job_info(self, job_id: str) -> Dict[str, Any]:
        """Return metadata for a scheduled job."""
        if job_id not in self._jobs:
            raise KeyError(f"Job '{job_id}' not found")
        job = self._jobs[job_id]
        return {
            "interval": job["interval"],
            "run_count": job["run_count"],
            "created_at": job["created_at"],
        }
