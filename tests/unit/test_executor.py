"""Tests for the Executor component."""

import pytest

from pipeline_runner.core.executor import Executor
from pipeline_runner.exceptions import ExecutionError


class TestExecutor:
    def test_execute_step_returns_result(self):
        executor = Executor(max_workers=2)
        result = executor.execute_step("step1", lambda: 42)
        assert result == 42
        executor.shutdown()

    def test_execute_step_with_exception(self):
        executor = Executor(max_workers=2)

        def failing():
            raise RuntimeError("boom")

        with pytest.raises(ExecutionError):
            executor.execute_step("step1", failing)
        executor.shutdown()

    def test_execute_pipeline(self):
        executor = Executor(max_workers=2)
        steps = [
            ("s1", lambda: 1, None),
            ("s2", lambda: 2, None),
        ]
        results = executor.execute_pipeline(steps)
        assert results == {"s1": 1, "s2": 2}
        executor.shutdown()
