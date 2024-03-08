"""Tests for pipeline models."""
import pytest
from datetime import datetime, timezone

from pipeline_runner.models.base import BaseModel
from pipeline_runner.models.step import Step
from pipeline_runner.models.pipeline import Pipeline
from pipeline_runner.models.trigger import Trigger


class TestBaseModel:
    def test_to_dict_serializes_datetimes(self):
        model = BaseModel()
        result = model.to_dict()
        assert isinstance(result["created_at"], str)
        assert "T" in result["created_at"]

    def test_from_dict_ignores_extra_keys(self):
        data = {"created_at": datetime.now(timezone.utc), "unknown": "value"}
        model = BaseModel.from_dict(data)
        assert not hasattr(model, "unknown")

    def test_validate_catches_none_fields(self):
        model = BaseModel(created_at=None)
        errors = model.validate()
        assert any("created_at" in e for e in errors)

    def test_validate_catches_empty_strings(self):
        pipeline = Pipeline(name="  ", description="valid")
        errors = pipeline.validate()
        assert any("empty" in e for e in errors)

    def test_touch_updates_timestamp(self):
        model = BaseModel()
        old_ts = model.updated_at
        model.touch()
        assert model.updated_at >= old_ts


class TestStep:
    def test_is_ready_no_deps(self):
        step = Step(id="s1", name="build", command="make")
        assert step.is_ready(set()) is True

    def test_is_ready_with_deps(self):
        step = Step(id="s2", name="test", command="pytest", depends_on=["s1"])
        assert step.is_ready(set()) is False
        assert step.is_ready({"s1"}) is True

    def test_is_terminal(self):
        step = Step(id="s1", name="build", command="make", status="succeeded")
        assert step.is_terminal() is True

    def test_lifecycle(self):
        step = Step(id="s1", name="build", command="make")
        step.start()
        assert step.status == "running"
        step.complete(success=True)
        assert step.status == "succeeded"


class TestTrigger:
    def test_matches_event(self):
        trigger = Trigger(source="github", event_type="push")
        assert trigger.matches("push") is True
        assert trigger.matches("pull_request") is False

    def test_matches_with_source(self):
        trigger = Trigger(source="github", event_type="push")
        assert trigger.matches("push", source="github") is True
        assert trigger.matches("push", source="gitlab") is False
