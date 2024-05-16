# Performance

## Benchmarks

Run the bundled benchmark harness from the repo root:

```bash
python scripts/benchmark.py --scenario default --iterations 20
```

Use `--json` for machine-readable output suitable for CI trend graphs. Compare results before and after config or code changes on identical hardware.

## Optimization tips

- **Worker pool sizing** — Set `PIPELINE_WORKER_CONCURRENCY` to roughly the number of CPU cores available per worker process if steps are CPU-bound; lower it if steps are I/O-bound and you run many replicas to avoid thrashing.
- **Local storage** — Point intermediate artifact directories to fast local SSD (`PIPELINE_LOCAL_CACHE_DIR`) so large blobs are not rewritten to remote storage on every step.
- **Async executors** — For I/O-heavy plugins, prefer async executors or batch APIs provided by the SDK so the worker thread pool is not blocked waiting on network round trips.

Monitor queue depth and p95 step duration in your metrics backend to validate changes.
