"""Tests for the StateMachine component."""

import pytest

from pipeline_runner.core.state_machine import StateMachine


class TestStateMachine:
    def test_initial_state(self):
        sm = StateMachine(
            states={"idle", "running", "done"},
            transitions={
                "idle": {"start": "running"},
                "running": {"finish": "done"},
            },
            initial_state="idle",
        )
        assert sm.current_state == "idle"

    def test_transition(self):
        sm = StateMachine(
            states={"idle", "running"},
            transitions={"idle": {"start": "running"}},
            initial_state="idle",
        )
        assert sm.transition("start") == "running"
        assert sm.current_state == "running"
        assert len(sm.history) == 1
        assert sm.history[0]["from"] == "idle"

    def test_invalid_transition_raises(self):
        sm = StateMachine(
            states={"idle", "running"},
            transitions={"idle": {"start": "running"}},
            initial_state="idle",
        )
        with pytest.raises(ValueError):
            sm.transition("stop")
