# Deployment

## Docker

Build and run from the repo root:

```bash
docker build -t pipeline-runner:latest -f docker/Dockerfile .
docker run --rm -e PIPELINE_QUEUE_URL -e PIPELINE_STORAGE_BUCKET pipeline-runner:latest
```

Prefer host networking disabled and a read-only root filesystem where supported. For local stacks, run `docker-compose -f docker-compose.yml up --build` from `deploy/`. Override `services.worker.environment` for queue URLs, object storage endpoints, and log levels.

## Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `PIPELINE_QUEUE_URL` | Yes | SQS or compatible queue endpoint |
| `PIPELINE_STORAGE_BUCKET` | Yes | Bucket for artifacts and logs |
| `PIPELINE_AUTH_TOKEN` | Yes in prod | Bearer token for API and worker auth |
| `PIPELINE_LOG_LEVEL` | No | Default `info` |
| `PIPELINE_WORKER_CONCURRENCY` | No | Parallel jobs per process (default `4`) |

## Production
Pin images by digest in orchestration manifests. Run workers behind a private network with egress restricted to your queue, storage, and OIDC issuer. Enable TLS, rotate `PIPELINE_AUTH_TOKEN`, ship logs to a centralized system, set CPU/memory limits per replica, and use `/healthz` before routing traffic.
