# Getting started with pipeline-runner

Install with pip (Python 3.10+):

```bash
pip install pipeline-runner
```

## Minimal example

```python
from pipeline_runner import Pipeline, Step

pipeline = Pipeline(name="demo")
pipeline.add_step(Step("echo", command=["echo", "hello"]))
print(pipeline.run().status)
```

Override `executor` on `Pipeline` if you need a custom backend.

## Configuration

These environment variables affect the embedded HTTP service and logging:

- **`SERVICE_NAME`** — e.g. `my-runner`; used in logs and metrics.
- **`PORT`** — e.g. `8080`; REST listen port.
- **`DEBUG`** — `true` / `1` for verbose output and stack traces.

Example: `export SERVICE_NAME=batch-worker PORT=9000 DEBUG=0`.

## Next steps

Use the configuration guide for `AppConfig` and `from_env()`, and the API reference for submitting and querying runs.
