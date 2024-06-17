# HTTP API reference

Base: `https://<host>:<port>`. JSON responses.

## GET /api/status

Probe for load balancers. Example: `GET /api/status` → `200` with body like `{"ok":true,"service":"pipeline-runner","version":"1.2.3"}`.

## POST /api/runs

Submit a run. Body: `{"pipeline":"deploy-app","parameters":{"env":"staging"}}`. Headers: `Content-Type: application/json`. Typical response: `202 Accepted` with `{"run_id":"run_01HQXYZ","status":"queued"}`.

## GET /api/runs/:id

Fetch one run. Example: `GET /api/runs/run_01HQXYZ` → `200` with:

```json
{"id":"run_01HQXYZ","status":"running","pipeline":"deploy-app","started_at":"2025-03-23T12:00:00Z"}
```

Use `GET /api/status` after deploys; use `POST` / `GET` runs for orchestration workflows.
