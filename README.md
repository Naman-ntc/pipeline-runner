[![CI](https://github.com/Naman-ntc/pipeline-runner/actions/workflows/ci.yml/badge.svg)](https://github.com/Naman-ntc/pipeline-runner/actions/workflows/ci.yml)

# pipeline-runner

A lightweight Python library and service for orchestrating CI-style pipelines: define a directed acyclic graph (DAG) of steps, run them with pluggable executors, and expose the same logic over HTTP or scheduled jobs.

## Features

- **DAG execution** — topological ordering, fan-out/fan-in, and explicit dependencies between steps
- **Pluggable backends** — swap local process execution, containers, or remote runners without changing pipeline definitions
- **Retry and backoff** — per-step policies for transient failures
- **ASGI endpoints** — embed pipeline control and status in any Starlette/FastAPI app
- **Webhooks** — trigger runs from Git hosting or chat integrations
- **Cron** — schedule recurring pipelines with standard cron expressions

## Requirements

- Python 3.10 or newer
- Optional: Docker or Podman when using container backends

## Installation

```bash
pip install pipeline-runner
```

For bleeding-edge builds:

```bash
pip install git+https://github.com/Naman-ntc/pipeline-runner.git
```

## Quick start

```python
from pipeline_runner import Pipeline, Executor

pipeline = Pipeline.from_yaml("deploy.yaml")
executor = Executor.from_env()
result = executor.run(pipeline, context={"env": "staging"})
print(result.status, result.step_results)
```

## CLI Usage

Run a pipeline by name using the bundled CLI:

```bash
pipeline-runner run --pipeline deploy
```

Inspect merged configuration (defaults, env, and file overlays):

```bash
pipeline-runner config show
```

List pipelines discovered from the configured search paths:

```bash
pipeline-runner pipeline list
```

## Run Requests

Programmatic runs use a structured request object that can be serialized for APIs and workers:

```python
from pipeline_runner.models.run import RunRequest

req = RunRequest(pipeline_name='deploy', trigger='manual')
payload = req.to_dict()
```

## Contributing

Bug reports, feature ideas, and pull requests are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) for development setup, coding conventions, and the review process.

## License

This project is licensed under the [MIT License](LICENSE).
