# Migration guide

## Upgrading to 0.1.0

Release **0.1.0** is the first semver-tagged stable line. Install with:

```bash
pip install pipeline-runner==0.1.0
```

## Compatibility

There are **no breaking changes** relative to the last published dev builds (`0.1.0.dev*`): pipeline YAML, plugin entry points, and environment variable names are unchanged. If you pinned a dev version, you can move to `0.1.0` without editing manifests.

## Configuration

Rename legacy optional keys if you still use pre-preview configs: `queue_url` → `PIPELINE_QUEUE_URL`, `storage_bucket` → `PIPELINE_STORAGE_BUCKET`. Old keys were accepted with deprecation warnings in dev; **0.1.0** drops those aliases—update `.env` or Helm values accordingly. Back up your database or state store before running bundled migrations if you use the optional metadata service.
