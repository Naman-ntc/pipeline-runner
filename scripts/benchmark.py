#!/usr/bin/env python3
"""Benchmark pipeline construction throughput."""

import argparse
import time

from pipeline_runner.core.pipeline import Pipeline


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.strip())
    p.add_argument("-n", "--count", type=int, default=1000)
    args = p.parse_args()
    t0 = time.perf_counter()
    for i in range(args.count):
        pipe = Pipeline()
        pipe.add_step(f"step-{i}", lambda: None)
    elapsed = time.perf_counter() - t0
    rate = args.count / elapsed if elapsed else 0.0
    print(f"throughput: {rate:.1f} pipelines/sec ({args.count} in {elapsed:.4f}s)")


if __name__ == "__main__":
    main()
