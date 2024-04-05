"""ASGI application entry point for the pipeline runner API."""
from __future__ import annotations

from pipeline_runner.config import get_config


async def app(scope, receive, send):
    if scope["type"] == "http" and scope["path"] == "/api/status":
        cfg = get_config()
        body = b'{"ok":true,"service":"' + cfg["service_name"].encode() + b'"}'
        await send({"type": "http.response.start", "status": 200, "headers": [[b"content-type", b"application/json"]]})
        await send({"type": "http.response.body", "body": body})
    else:
        await send({"type": "http.response.start", "status": 404, "headers": []})
        await send({"type": "http.response.body", "body": b"not found"})
