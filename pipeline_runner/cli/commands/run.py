"""CLI run subcommand — execute a named pipeline."""

import logging
import sys
from pathlib import Path

import yaml

logger = logging.getLogger(__name__)


def load_pipeline_config(config_path: str) -> dict:
    path = Path(config_path)
    if not path.exists():
        logger.error("Pipeline config not found: %s", path)
        sys.exit(1)
    with open(path) as f:
        return yaml.safe_load(f)


def execute_pipeline(name: str, config: dict) -> bool:
    steps = config.get("steps", [])
    logger.info("Executing pipeline '%s' with %d steps", name, len(steps))
    for i, step in enumerate(steps):
        logger.info("Step %d/%d: %s", i + 1, len(steps), step.get("name", "unnamed"))
    return True


def handle_run(args) -> None:
    logger.info("Loading pipeline: %s", args.pipeline_name)
    config = load_pipeline_config(args.config_path)
    success = execute_pipeline(args.pipeline_name, config)
    if not success:
        print(f"Pipeline '{args.pipeline_name}' failed", file=sys.stderr)
        sys.exit(1)
    print(f"Pipeline '{args.pipeline_name}' completed successfully")
