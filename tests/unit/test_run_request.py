"""Tests for run request models."""

from pipeline_runner.models.run import RunRequest, RunStatus


def test_create():
    req = RunRequest(pipeline_name="ci-deploy")
    assert req.pipeline_name == "ci-deploy"
    assert req.status == RunStatus.PENDING


def test_to_dict():
    req = RunRequest(pipeline_name="nightly")
    data = req.to_dict()
    assert "pipeline_name" in data
    assert "status" in data
    assert data["pipeline_name"] == "nightly"
    assert data["status"] in (RunStatus.PENDING, RunStatus.PENDING.value)


def test_sanitizes():
    req = RunRequest(pipeline_name="  trim-me  ")
    assert req.pipeline_name == "trim-me"
