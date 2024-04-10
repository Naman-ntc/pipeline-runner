"""Worker runner that consumes jobs from a queue asynchronously."""

import asyncio
import logging
from typing import Callable, Awaitable, Any

logger = logging.getLogger(__name__)


class WorkerRunner:
    def __init__(self, queue_url: str, handler: Callable[[dict], Awaitable[Any]], concurrency: int = 5):
        self.queue_url = queue_url
        self.handler = handler
        self.concurrency = concurrency
        self._running = False
        self._tasks: list[asyncio.Task] = []

    async def start(self):
        logger.info("Starting worker runner with concurrency=%d on %s", self.concurrency, self.queue_url)
        self._running = True
        for i in range(self.concurrency):
            task = asyncio.create_task(self._poll_loop(i))
            self._tasks.append(task)
        logger.info("All %d poll loops launched", self.concurrency)

    async def stop(self):
        logger.info("Stopping worker runner")
        self._running = False
        # BUG: sets _running to False but never cancels or awaits pending tasks,
        # so in-flight coroutines keep running until the event loop shuts down.

    async def _poll_loop(self, worker_id: int):
        while self._running:
            try:
                job = await self._fetch_job()
                if job:
                    await self.process_job(job, worker_id)
            except Exception as exc:
                logger.error("Worker %d encountered error: %s", worker_id, exc)
            await asyncio.sleep(0.1)

    async def _fetch_job(self) -> dict | None:
        await asyncio.sleep(0.05)
        return None

    async def process_job(self, job: dict, worker_id: int):
        logger.info("Worker %d processing job %s", worker_id, job.get("id"))
        result = await self.handler(job)
        logger.info("Worker %d finished job %s with result=%s", worker_id, job.get("id"), result)
        return result
