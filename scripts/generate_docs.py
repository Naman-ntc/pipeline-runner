#!/usr/bin/env python3
"""Extract docstrings from pipeline_runner for quick reference."""

import argparse
import ast
from pathlib import Path


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.strip())
    p.add_argument("--root", type=Path, default=Path("pipeline_runner"))
    for path in sorted(p.parse_args().root.rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                doc = ast.get_docstring(node)
                if doc:
                    print(f"{path}:{node.lineno} {node.name}")
                    print(doc)
                    print()


if __name__ == "__main__":
    main()
