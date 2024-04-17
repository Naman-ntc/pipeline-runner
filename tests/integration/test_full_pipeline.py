"""Tests for Pipeline validation (commit 74)."""

from pipeline_runner.core import Pipeline


def test_pipeline_single_step():
    ran: list = []
    p = Pipeline("test")
    p.add_step("step1", lambda: ran.append(True))
    assert p.validate() == []
