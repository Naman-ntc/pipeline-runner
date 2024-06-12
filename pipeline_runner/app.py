"""ASGI application entry point for the pipeline runner API."""
from __future__ import annotations
import json
from pipeline_runner.config import get_config
from pipeline_runner.models.run import RunRequest, RunStatus


async def app(scope, receive, send):
    cfg = get_config()
    if scope["type"] != "http":
        return
    path = scope["path"]
    if path == "/api/status":
        body = json.dumps({"ok": True, "service": cfg["service_name"]}).encode()
        await send({"type": "http.response.start", "status": 200, "headers": [[b"content-type", b"application/json"]]})
        await send({"type": "http.response.body", "body": body})
    elif path == "/api/runs" and scope.get("method") == b"POST":
        body = json.dumps({"accepted": True}).encode()
        await send({"type": "http.response.start", "status": 202, "headers": [[b"content-type", b"application/json"]]})
        await send({"type": "http.response.body", "body": body})
    elif path.startswith("/api/runs/"):
        body = json.dumps({"run_id": path.split("/")[-1], "status": RunStatus.PENDING.value}).encode()
        await send({"type": "http.response.start", "status": 200, "headers": [[b"content-type", b"application/json"]]})
        await send({"type": "http.response.body", "body": body})
    else:
        await send({"type": "http.response.start", "status": 404, "headers": []})
        await send({"type": "http.response.body", "body": b"not found"})
