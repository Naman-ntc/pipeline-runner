"""Entry point for running the pipeline runner as a module."""

import asyncio
import logging
import sys

from pipeline_runner.workers.runner import WorkerRunner
from pipeline_runner.workers.heartbeat import HeartbeatEmitter
from pipeline_runner.workers.pool import WorkerPool

logger = logging.getLogger(__name__)


async def default_handler(job: dict) -> dict:
    logger.info("Processing job: %s", job.get("id", "unknown"))
    return {"status": "completed", "job_id": job.get("id")}


def health_callback() -> dict:
    return {"status": "healthy", "uptime_seconds": 0}


async def run():
    pool = WorkerPool(min_workers=2, max_workers=8)
    heartbeat = HeartbeatEmitter(interval=10.0, callback=health_callback)
    runner = WorkerRunner(
        queue_url="amqp://localhost:5672/jobs",
        handler=default_handler,
        concurrency=4,
    )
    heartbeat.start()
    await runner.start()
    try:
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    finally:
        await runner.stop()
        heartbeat.stop()
        await pool.shutdown()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
    asyncio.run(run())
