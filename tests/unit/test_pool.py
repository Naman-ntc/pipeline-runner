"""Unit tests for the worker pool module."""

import asyncio
import pytest
from pipeline_runner.workers.pool import WorkerPool


@pytest.mark.asyncio
async def test_pool_submit_and_count():
    pool = WorkerPool(min_workers=1, max_workers=5)
    async def dummy_work():
        await asyncio.sleep(10)
    await pool.submit(dummy_work)
    await pool.submit(dummy_work)
    assert pool.active_count == 2
    await pool.shutdown()
    assert pool.active_count == 0


@pytest.mark.asyncio
async def test_pool_scale_up_respects_max():
    pool = WorkerPool(min_workers=1, max_workers=3)
    async def noop():
        await asyncio.sleep(10)
    await pool.scale_up(noop, count=5)
    assert len(pool._workers) == 3
    await pool.shutdown()
