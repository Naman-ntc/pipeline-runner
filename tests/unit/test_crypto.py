"""Tests for concurrency and health utilities."""
from pipeline_runner.utils.concurrency import run_parallel, SemaphoreWrapper
from pipeline_runner.utils.health import HealthStatus, HealthChecker


class TestRunParallel:
    def test_preserves_order(self):
        items = [1, 2, 3, 4, 5]
        results = run_parallel(items, lambda x: x * 2, max_workers=2)
        assert results == [2, 4, 6, 8, 10]

    def test_empty_input(self):
        results = run_parallel([], lambda x: x)
        assert results == []


class TestSemaphoreWrapper:
    def test_context_manager(self):
        sem = SemaphoreWrapper(1)
        with sem:
            pass


class TestHealthChecker:
    def test_all_healthy(self):
        checker = HealthChecker()
        checker.add_check("db", lambda: True)
        status, failures = checker.run_checks()
        assert status == HealthStatus.HEALTHY
        assert failures == []

    def test_degraded(self):
        checker = HealthChecker()
        checker.add_check("db", lambda: True)
        checker.add_check("cache", lambda: False)
        status, failures = checker.run_checks()
        assert status == HealthStatus.DEGRADED
        assert "cache" in failures
