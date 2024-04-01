"""Tests for the Scheduler component."""

import pytest

from pipeline_runner.core.scheduler import Scheduler


class TestScheduler:
    def test_schedule_and_list(self):
        s = Scheduler()
        s.schedule("job1", lambda: None, 10.0)
        assert "job1" in s.list_jobs()

    def test_unschedule(self):
        s = Scheduler()
        s.schedule("job1", lambda: None, 10.0)
        s.unschedule("job1")
        assert "job1" not in s.list_jobs()

    def test_tick_immediate(self):
        s = Scheduler()
        results = []
        s.schedule("job1", lambda: results.append(1), 60.0, immediate=True)
        executed = s.tick()
        assert "job1" in executed
        assert results == [1]
