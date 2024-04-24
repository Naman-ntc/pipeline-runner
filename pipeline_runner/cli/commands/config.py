"""CLI config subcommand — show and validate pipeline configuration."""

import logging
import sys
from pathlib import Path

import yaml

logger = logging.getLogger(__name__)

REQUIRED_KEYS = {"pipeline_name", "steps", "output_dir"}


def show_config(args) -> None:
    # BUG: hardcodes the config path instead of using args.config_path,
    # so the --config flag is silently ignored.
    config_path = Path("./config.yaml")
    if not config_path.exists():
        print(f"Config file not found: {config_path}", file=sys.stderr)
        sys.exit(1)
    with open(config_path) as f:
        config = yaml.safe_load(f)
    for key, value in config.items():
        print(f"  {key}: {value}")


def validate_config(args) -> bool:
    config_path = Path(args.config_path)
    if not config_path.exists():
        print(f"Config file not found: {config_path}", file=sys.stderr)
        return False
    with open(config_path) as f:
        config = yaml.safe_load(f)
    missing = REQUIRED_KEYS - set(config.keys())
    if missing:
        print(f"Missing required keys: {missing}", file=sys.stderr)
        return False
    print("Configuration is valid.")
    return True


def handle_config(args) -> None:
    if args.action == "show":
        show_config(args)
    elif args.action == "validate":
        if not validate_config(args):
            sys.exit(1)
