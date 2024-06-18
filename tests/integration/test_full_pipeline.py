"""Tests for Pipeline validation and run requests (commit 177, feat)."""

from pipeline_runner.core import Pipeline
from pipeline_runner.models.run import RunRequest, RunStatus


def test_pipeline_single_step():
    ran: list = []
    p = Pipeline("test")
    p.add_step("step1", lambda: ran.append(True))
    assert p.validate() == []


def test_run_request_creation():
    req = RunRequest(pipeline_name="deploy", trigger="manual")
    assert req.status is RunStatus.PENDING
