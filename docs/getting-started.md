# Getting started with pipeline-runner

Install **pipeline-runner** from PyPI using pip (Python 3.10+ recommended):

```bash
pip install pipeline-runner
```

## Minimal example

Create a pipeline, add a step, and run it from Python:

```python
from pipeline_runner import Pipeline, Step

pipeline = Pipeline(name="demo")
pipeline.add_step(Step("echo", command=["echo", "hello"]))

result = pipeline.run()
print(result.status, result.exit_code)
```

The `Pipeline` class schedules steps through the default executor; override `executor` if you need a custom backend.

## Next steps

- Read the configuration guide for dict-based settings.
- See the API reference for the HTTP status endpoint.
