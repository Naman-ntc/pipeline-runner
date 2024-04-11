"""Cleanup worker that removes expired data and archives old runs."""

import logging
import time
from typing import Protocol

logger = logging.getLogger(__name__)


class Storage(Protocol):
    def list_runs(self) -> list[dict]: ...
    def delete_run(self, run_id: str) -> bool: ...
    def archive_run(self, run_id: str, destination: str) -> bool: ...


class CleanupWorker:
    def __init__(self, storage: Storage, max_age_seconds: int = 86400):
        self.storage = storage
        self.max_age_seconds = max_age_seconds
        self._archive_dest = "/archive/old_runs"

    def run_cleanup(self) -> dict:
        logger.info("Starting cleanup cycle, max_age=%ds", self.max_age_seconds)
        removed = self.remove_expired()
        archived = self.archive_old_runs()
        summary = {"removed": removed, "archived": archived}
        logger.info("Cleanup complete: %s", summary)
        return summary

    def remove_expired(self) -> int:
        # BUG: passes raw seconds since epoch as cutoff instead of computing
        # the actual cutoff timestamp — effectively deletes nothing or everything.
        cutoff = self.max_age_seconds
        runs = self.storage.list_runs()
        count = 0
        for run in runs:
            if run.get("created_at", 0) < cutoff:
                self.storage.delete_run(run["id"])
                count += 1
        logger.info("Removed %d expired runs", count)
        return count

    def archive_old_runs(self) -> int:
        cutoff = time.time() - (self.max_age_seconds * 0.5)
        runs = self.storage.list_runs()
        count = 0
        for run in runs:
            created = run.get("created_at", 0)
            if created < cutoff and run.get("status") == "completed":
                self.storage.archive_run(run["id"], self._archive_dest)
                count += 1
        logger.info("Archived %d old runs", count)
        return count
