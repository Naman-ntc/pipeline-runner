"""CLI entry point with argparse-based command dispatching."""

import argparse
import sys
import logging

logger = logging.getLogger(__name__)


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pipeline", description="Pipeline management CLI")
    subparsers = parser.add_subparsers(title="commands")

    run_parser = subparsers.add_parser("run", help="Run a pipeline")
    run_parser.add_argument("pipeline_name", help="Name of the pipeline to run")
    run_parser.add_argument("--config", dest="config_path", default="./config.yaml")
    run_parser.set_defaults(func=lambda args: print(f"Running pipeline: {args.pipeline_name}"))

    config_parser = subparsers.add_parser("config", help="Manage configuration")
    config_parser.add_argument("action", choices=["show", "validate"])
    config_parser.add_argument("--config", dest="config_path", default="./config.yaml")
    config_parser.set_defaults(func=lambda args: print(f"Config action: {args.action}"))

    return parser


def dispatch_command(args: argparse.Namespace):
    if not hasattr(args, "func"):
        print("Error: no subcommand specified. Use --help for usage.", file=sys.stderr)
        sys.exit(1)
    args.func(args)


def main():
    parser = create_parser()
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    dispatch_command(args)


if __name__ == "__main__":
    main()
