"""Worker pool lifecycle tests (commit 89)."""

from pipeline_runner.workers.pool import WorkerPool


def test_pool_creation():
    pool = WorkerPool(min_workers=2, max_workers=8)
    assert pool.active_count == 0
