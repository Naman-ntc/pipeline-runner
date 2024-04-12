"""Unit tests for the worker runner and heartbeat modules."""

import asyncio
import pytest
from unittest.mock import AsyncMock, MagicMock
from pipeline_runner.workers.runner import WorkerRunner
from pipeline_runner.workers.heartbeat import HeartbeatEmitter


@pytest.mark.asyncio
async def test_worker_runner_start_stop():
    handler = AsyncMock(return_value={"status": "ok"})
    runner = WorkerRunner("amqp://localhost/test", handler, concurrency=2)
    await runner.start()
    assert runner._running is True
    assert len(runner._tasks) == 2
    await runner.stop()
    assert runner._running is False


@pytest.mark.asyncio
async def test_worker_runner_process_job():
    handler = AsyncMock(return_value={"result": 42})
    runner = WorkerRunner("amqp://localhost/test", handler, concurrency=1)
    result = await runner.process_job({"id": "job-1", "data": "payload"}, 0)
    handler.assert_awaited_once()
    assert result == {"result": 42}


def test_heartbeat_emitter_emit():
    callback = MagicMock(return_value={"status": "healthy", "cpu": 0.5})
    emitter = HeartbeatEmitter(interval=5.0, callback=callback)
    health = emitter.emit()
    callback.assert_called_once()
    assert health["status"] == "healthy"
    assert emitter.check_health() == health
