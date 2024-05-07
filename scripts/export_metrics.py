#!/usr/bin/env python3
"""Export metrics snapshot as JSON (stdout)."""

import argparse
import json

from pipeline_runner.core.metrics import MetricsCollector


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.strip())
    p.add_argument("--compact", action="store_true", help="minified JSON")
    args = p.parse_args()
    collector = MetricsCollector()
    collector.counter("pipelines.started", 2)
    collector.gauge("workers.active", 4.0)
    payload = collector.export()
    kwargs = {"separators": (",", ":")} if args.compact else {"indent": 2}
    print(json.dumps(payload, **kwargs))


if __name__ == "__main__":
    main()
