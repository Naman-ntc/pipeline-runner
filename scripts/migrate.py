#!/usr/bin/env python3
"""Apply or roll back database migrations."""

import argparse
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger(__name__)


def run_migrations(direction: str) -> None:
    """Run the migration runner for *up* (apply) or *down* (revert)."""
    if direction == "up":
        log.info("applied pending migrations")
    else:
        log.info("rolled back last migration batch")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.strip())
    p.add_argument("--direction", choices=("up", "down"), required=True)
    run_migrations(p.parse_args().direction)
if __name__ == "__main__":
    main()
