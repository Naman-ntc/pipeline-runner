"""Unit tests for the retry handler module."""

import asyncio
import pytest
from unittest.mock import AsyncMock
from pipeline_runner.workers.retry import RetryHandler


@pytest.mark.asyncio
async def test_retry_succeeds_first_attempt():
    handler = RetryHandler(max_retries=3, base_delay=0.01)
    func = AsyncMock(return_value="done")
    result = await handler.execute_with_retry("job-1", func)
    assert result == "done"
    func.assert_awaited_once()


@pytest.mark.asyncio
async def test_retry_recovers_after_failures():
    handler = RetryHandler(max_retries=3, base_delay=0.01)
    func = AsyncMock(side_effect=[ValueError("fail"), ValueError("fail"), "ok"])
    result = await handler.execute_with_retry("job-2", func)
    assert result == "ok"
    assert func.await_count == 3


@pytest.mark.asyncio
async def test_retry_exhausted_raises():
    handler = RetryHandler(max_retries=2, base_delay=0.01)
    func = AsyncMock(side_effect=RuntimeError("always fails"))
    with pytest.raises(RuntimeError, match="always fails"):
        await handler.execute_with_retry("job-3", func)
    assert func.await_count == 3
