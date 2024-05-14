"""Pipeline orchestration combining dependency graph and executor."""

import logging
from typing import Any, Callable, Dict, List, Optional

from pipeline_runner.core.dependency_graph import DependencyGraph
from pipeline_runner.core.executor import Executor
from pipeline_runner.exceptions import PipelineError

logger = logging.getLogger(__name__)


class Pipeline:
    """Orchestrates step execution respecting dependency ordering."""

    def __init__(self, max_workers: int = 4) -> None:
        self._steps: Dict[str, Callable] = {}
        self._timeouts: Dict[str, Optional[float]] = {}
        self._deps: Dict[str, List[str]] = {}
        self._graph = DependencyGraph()
        self._executor = Executor(max_workers=max_workers)

    def add_step(
        self,
        step_id: str,
        step_fn: Callable,
        depends_on: Optional[List[str]] = None,
        timeout: Optional[float] = None,
    ) -> None:
        """Add a step to the pipeline with optional dependencies."""
        self._steps[step_id] = step_fn
        self._timeouts[step_id] = timeout
        self._deps[step_id] = list(depends_on or [])

    def remove_step(self, step_id: str) -> None:
        """Remove a step from the pipeline."""
        if step_id not in self._steps:
            raise PipelineError(f"Step '{step_id}' not found")
        del self._steps[step_id]
        del self._timeouts[step_id]
        del self._deps[step_id]

    def _build_graph(self) -> None:
        """Reconstruct the dependency graph from current steps."""
        self._graph = DependencyGraph()
        for step_id in self._steps:
            self._graph.add_node(step_id)
        for step_id, deps in self._deps.items():
            for dep in deps:
                if dep in self._steps:
                    self._graph.add_edge(step_id, dep)

    def validate(self) -> List[str]:
        """Validate the pipeline configuration. Returns a list of warnings.

        FIX: now also detects dependency cycles via detect_cycles().
        """
        warnings: List[str] = []
        if not self._steps:
            warnings.append("Pipeline has no steps")
            return warnings
        for step_id, deps in self._deps.items():
            for dep in deps:
                if dep not in self._steps:
                    warnings.append(
                        f"Step '{step_id}' depends on unknown step '{dep}'"
                    )
        self._build_graph()
        cycles = self._graph.detect_cycles()
        if cycles:
            warnings.append(
                f"Pipeline contains {len(cycles)} cycle(s)"
            )
        return warnings

    def run(self) -> Dict[str, Any]:
        """Execute the pipeline in dependency order."""
        warnings = self.validate()
        for w in warnings:
            logger.warning(w)
        self._build_graph()
        order = self._graph.topological_sort()
        results: Dict[str, Any] = {}
        for step_id in order:
            step_fn = self._steps[step_id]
            timeout = self._timeouts.get(step_id)
            results[step_id] = self._executor.execute_step(
                step_id, step_fn, timeout
            )
        return results

    def shutdown(self) -> None:
        """Clean up executor resources."""
        self._executor.shutdown()
