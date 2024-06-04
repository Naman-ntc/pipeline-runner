"""ASGI application entry point for the pipeline runner API."""
from __future__ import annotations
import json
from pipeline_runner.config import get_config
from pipeline_runner.auth.decorators import require_auth


@require_auth
async def _status(scope, receive, send):
    cfg = get_config()
    body = json.dumps({"ok": True, "service": cfg.service_name}).encode()
    await send({"type": "http.response.start", "status": 200, "headers": [[b"content-type", b"application/json"]]})
    await send({"type": "http.response.body", "body": body})


async def app(scope, receive, send):
    if scope["type"] == "http" and scope["path"] == "/api/status":
        await _status(scope, receive, send)
    else:
        await send({"type": "http.response.start", "status": 404, "headers": []})
        await send({"type": "http.response.body", "body": b"not found"})
