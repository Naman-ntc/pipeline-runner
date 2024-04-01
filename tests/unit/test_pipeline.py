"""Tests for the Pipeline component."""

import pytest

from pipeline_runner.core.pipeline import Pipeline
from pipeline_runner.exceptions import PipelineError


class TestPipeline:
    def test_add_and_run_single_step(self):
        p = Pipeline(max_workers=1)
        p.add_step("s1", lambda: "result")
        results = p.run()
        assert results["s1"] == "result"
        p.shutdown()

    def test_remove_missing_step_raises(self):
        p = Pipeline(max_workers=1)
        with pytest.raises(PipelineError):
            p.remove_step("nonexistent")

    def test_validate_empty_pipeline(self):
        p = Pipeline(max_workers=1)
        warnings = p.validate()
        assert any("no steps" in w.lower() for w in warnings)

    def test_validate_missing_dependency(self):
        p = Pipeline(max_workers=1)
        p.add_step("s1", lambda: None, depends_on=["missing"])
        warnings = p.validate()
        assert any("unknown" in w.lower() for w in warnings)
        p.shutdown()

    def test_run_with_dependencies(self):
        p = Pipeline(max_workers=1)
        order = []
        p.add_step("a", lambda: order.append("a"))
        p.add_step("b", lambda: order.append("b"), depends_on=["a"])
        p.run()
        assert order.index("a") < order.index("b")
        p.shutdown()
