# Contributing to pipeline-runner

Thanks for helping improve pipeline-runner. Below: setup, tests, style, and how we merge changes.

## Development setup

```bash
git clone https://github.com/pipeline-runner/pipeline-runner.git
cd pipeline-runner
pip install -e ".[dev]"
```

Use a virtual environment (`python -m venv .venv`, then activate) before installing.

## Running tests

Run `make test` (runs `pytest -v`). Fix failures before opening a PR.

## Code style

Follow **PEP 8**, add **type hints** where they help, and use concise **docstrings** for public APIs. Run `make lint` and `make format` before submitting so CI stays green.

## Pull request process

Fork, branch from `main`, keep commits focused, and open a PR describing the problem and fix. Address review feedback; we merge when the change is ready.
