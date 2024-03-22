"""Finite state machine implementation."""

from typing import Dict, List, Set


class StateMachine:
    """Simple finite state machine with transition history tracking."""

    def __init__(
        self,
        states: Set[str],
        transitions: Dict[str, Dict[str, str]],
        initial_state: str,
    ) -> None:
        if initial_state not in states:
            raise ValueError(
                f"Initial state '{initial_state}' not in defined states"
            )
        self._states = frozenset(states)
        self._transitions = transitions
        self._current_state = initial_state
        self._history: List[Dict[str, str]] = []

        for state, events in transitions.items():
            if state not in states:
                raise ValueError(
                    f"Transition source '{state}' not in states"
                )
            for event, target in events.items():
                if target not in states:
                    raise ValueError(
                        f"Target state '{target}' for event '{event}' "
                        f"from '{state}' not in defined states"
                    )

    @property
    def current_state(self) -> str:
        """Return the current state."""
        return self._current_state

    @property
    def history(self) -> List[Dict[str, str]]:
        """Return a copy of the transition history."""
        return list(self._history)

    def transition(self, event: str) -> str:
        """Attempt to transition based on the given event.

        Returns the new state after transition.
        Raises ValueError if no transition exists for the event.
        """
        state_transitions = self._transitions.get(self._current_state, {})
        if event not in state_transitions:
            raise ValueError(
                f"No transition for event '{event}' "
                f"from state '{self._current_state}'"
            )
        previous = self._current_state
        self._current_state = state_transitions[event]
        self._history.append({
            "from": previous,
            "event": event,
            "to": self._current_state,
        })
        return self._current_state

    @property
    def available_events(self) -> List[str]:
        """Return events available from the current state."""
        return list(self._transitions.get(self._current_state, {}).keys())

    @property
    def states(self) -> frozenset:
        """Return the set of all defined states."""
        return self._states
