"""Dynamic worker pool with scaling capabilities."""

import asyncio
import logging
from typing import Callable, Awaitable

logger = logging.getLogger(__name__)


class WorkerPool:
    def __init__(self, min_workers: int = 2, max_workers: int = 10):
        self.min_workers = min_workers
        self.max_workers = max_workers
        self._workers: list[asyncio.Task] = []
        self._shutting_down = False

    @property
    def active_count(self) -> int:
        return len([t for t in self._workers if not t.done()])

    async def submit(self, coro: Callable[[], Awaitable]) -> asyncio.Task:
        if self._shutting_down:
            raise RuntimeError("Pool is shutting down, cannot submit new work")
        task = asyncio.create_task(coro())
        self._workers.append(task)
        logger.info("Submitted task, pool size=%d", len(self._workers))
        return task

    async def shutdown(self):
        self._shutting_down = True
        logger.info("Shutting down pool with %d workers", len(self._workers))
        for task in self._workers:
            task.cancel()
        await asyncio.gather(*self._workers, return_exceptions=True)
        self._workers.clear()

    async def scale_up(self, coro_factory: Callable[[], Awaitable], count: int = 1):
        for _ in range(count):
            if len(self._workers) >= self.max_workers:
                logger.warning("At max capacity (%d), cannot scale up", self.max_workers)
                break
            await self.submit(coro_factory)

    async def scale_down(self, count: int = 1):
        if len(self._workers) <= self.min_workers:
            logger.warning("At min capacity (%d), cannot scale down", self.min_workers)
            return
        # BUG: logs the intent but never actually cancels any worker tasks.
        to_remove = min(count, len(self._workers) - self.min_workers)
        logger.info("Scaling down by %d workers", to_remove)
