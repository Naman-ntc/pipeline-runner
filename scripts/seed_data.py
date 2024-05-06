#!/usr/bin/env python3
"""Seed sample pipeline definitions for local development."""

import json
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger(__name__)


def build_sample_pipeline() -> dict:
    return {
        "name": "demo",
        "version": 1,
        "steps": [
            {"id": "fetch", "cmd": "curl -fsS https://example.com"},
            {"id": "parse", "cmd": "jq ."},
        ],
    }


if __name__ == "__main__":
    sample = build_sample_pipeline()
    log.info("seeded %s step(s)", len(sample["steps"]))
    print(json.dumps(sample, indent=2))
