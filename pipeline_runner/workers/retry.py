"""Retry handler with exponential backoff for failed worker jobs."""

import asyncio
import logging
import random
from typing import Callable, Awaitable, Any

logger = logging.getLogger(__name__)


class RetryHandler:
    def __init__(self, max_retries: int = 3, base_delay: float = 1.0, max_delay: float = 30.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self._retry_counts: dict[str, int] = {}

    async def execute_with_retry(self, job_id: str, func: Callable[[], Awaitable[Any]]) -> Any:
        self._retry_counts[job_id] = 0
        last_exc: Exception | None = None
        for attempt in range(self.max_retries + 1):
            try:
                result = await func()
                self._retry_counts.pop(job_id, None)
                return result
            except Exception as exc:
                last_exc = exc
                self._retry_counts[job_id] = attempt + 1
                if attempt < self.max_retries:
                    delay = self._calculate_delay(attempt)
                    logger.warning("Job %s attempt %d failed, retrying in %.1fs: %s",
                                   job_id, attempt + 1, delay, exc)
                    await asyncio.sleep(delay)
        self._retry_counts.pop(job_id, None)
        raise last_exc  # type: ignore[misc]

    def _calculate_delay(self, attempt: int) -> float:
        delay = self.base_delay * (2 ** attempt)
        jitter = random.uniform(0, delay * 0.1)
        return min(delay + jitter, self.max_delay)

    def get_retry_count(self, job_id: str) -> int:
        return self._retry_counts.get(job_id, 0)
