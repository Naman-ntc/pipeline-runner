"""CLI pipeline subcommand — list and inspect pipeline definitions."""

import logging
from pathlib import Path

import yaml

logger = logging.getLogger(__name__)

DEFAULT_PIPELINES_DIR = "./pipelines"


def list_pipelines(pipelines_dir: str = DEFAULT_PIPELINES_DIR) -> list[dict]:
    path = Path(pipelines_dir)
    if not path.is_dir():
        logger.warning("Pipelines directory not found: %s", path)
        return []
    pipelines = []
    for yaml_file in sorted(path.glob("*.yaml")):
        with open(yaml_file) as f:
            data = yaml.safe_load(f)
        pipelines.append({
            "name": data.get("pipeline_name", yaml_file.stem),
            "steps": len(data.get("steps", [])),
            "file": str(yaml_file),
        })
    return pipelines


def handle_pipeline(args) -> None:
    if args.action == "list":
        pipelines = list_pipelines(getattr(args, "pipelines_dir", DEFAULT_PIPELINES_DIR))
        if not pipelines:
            print("No pipelines found.")
            return
        for p in pipelines:
            print(f"  {p['name']} ({p['steps']} steps) — {p['file']}")
    elif args.action == "inspect":
        print(f"Inspecting pipeline: {args.pipeline_name}")
