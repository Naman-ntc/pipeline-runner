"""Step executor using thread pool for concurrent pipeline execution."""

import logging
from concurrent.futures import Future, ThreadPoolExecutor, TimeoutError
from typing import Any, Callable, Dict, List, Optional, Tuple

from pipeline_runner.exceptions import ExecutionError

logger = logging.getLogger(__name__)


class Executor:
    """Executes pipeline steps concurrently using a thread pool."""

    def __init__(self, max_workers: int = 4) -> None:
        self._max_workers = max_workers
        self._pool = ThreadPoolExecutor(max_workers=max_workers)
        self._futures: Dict[str, Future] = {}

    def execute_step(
        self,
        step_id: str,
        step_fn: Callable[[], Any],
        timeout: Optional[float] = None,
    ) -> Any:
        """Submit a step for execution and return its result."""
        future = self._pool.submit(step_fn)
        self._futures[step_id] = future
        try:
            return future.result(timeout=timeout)
        except TimeoutError:
            # FIX: include step_id in the error message
            raise ExecutionError(f"Step '{step_id}' timed out")
        except Exception as exc:
            raise ExecutionError(
                f"Step '{step_id}' failed: {exc}"
            ) from exc

    def execute_pipeline(
        self, steps: List[Tuple[str, Callable[[], Any], Optional[float]]]
    ) -> Dict[str, Any]:
        """Execute a sequence of steps and return results keyed by step_id."""
        results: Dict[str, Any] = {}
        for step_id, step_fn, timeout in steps:
            results[step_id] = self.execute_step(step_id, step_fn, timeout)
        return results

    def gather_results(self, futures: Dict[str, Future]) -> Dict[str, Any]:
        """Wait for submitted futures and collect their results."""
        results: Dict[str, Any] = {}
        for step_id, future in futures.items():
            try:
                results[step_id] = future.result()
            except Exception as exc:
                raise ExecutionError(
                    f"Step '{step_id}' failed: {exc}"
                ) from exc
        return results

    def shutdown(self, wait: bool = True) -> None:
        """Shut down the thread pool."""
        self._pool.shutdown(wait=wait)
        self._futures.clear()
