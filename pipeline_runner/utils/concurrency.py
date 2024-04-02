"""Concurrency utilities for parallel task execution."""
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Callable, List, Sequence, TypeVar

T = TypeVar("T")
R = TypeVar("R")


def run_parallel(
    items: Sequence[T],
    fn: Callable[[T], R],
    max_workers: int = 4,
) -> List[R]:
    """Execute fn on each item in parallel, returning results in order."""
    results: List[Any] = [None] * len(items)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_idx = {
            executor.submit(fn, item): idx
            for idx, item in enumerate(items)
        }
        for future in as_completed(future_to_idx):
            idx = future_to_idx[future]
            results[idx] = future.result()
    return results


class SemaphoreWrapper:
    """Context manager wrapping a threading.Semaphore."""

    def __init__(self, limit: int) -> None:
        self._sem = threading.Semaphore(limit)

    def __enter__(self) -> "SemaphoreWrapper":
        self._sem.acquire()
        return self

    def __exit__(self, *args) -> None:
        self._sem.release()
