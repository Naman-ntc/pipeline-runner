import time
import logging
from typing import Callable

logger = logging.getLogger(__name__)


class LoggingMiddleware:
    def __init__(self, app: Callable) -> None:
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            start = time.monotonic()
            path = scope.get("path", "/")
            method = scope.get("method", "?")
            logger.info("Incoming %s %s", method, path)
            await self.app(scope, receive, send)
            elapsed = time.monotonic() - start
            logger.info("%s %s completed in %.3fs", method, path, elapsed)
        else:
            await self.app(scope, receive, send)


class CORSMiddleware:
    def __init__(self, app: Callable, allowed_origins: list[str] | None = None) -> None:
        self.app = app
        self.allowed_origins = allowed_origins or ["*"]

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        async def wrapped_send(message):
            if message["type"] == "http.response.start":
                headers = list(message.get("headers", []))
                origin = self.allowed_origins[0]
                headers.append((b"access-control-allow-origin", origin.encode()))
                headers.append((b"access-control-allow-methods", b"GET,POST,PUT,DELETE,OPTIONS"))
                headers.append((b"access-control-allow-headers", b"Content-Type,Authorization"))
                message["headers"] = headers
            await send(message)

        await self.app(scope, receive, wrapped_send)


class AuthMiddleware:
    def __init__(self, app: Callable, secret_key: str) -> None:
        self.app = app
        self.secret_key = secret_key

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        headers = dict(scope.get("headers", []))
        token = headers.get(b"authorization", b"").decode()
        scope["user"] = None
        if token.startswith("Bearer "):
            scope["user"] = self._decode(token[7:])
        await self.app(scope, receive, send)

    def _decode(self, token: str) -> dict | None:
        parts = token.split(".")
        if len(parts) == 2:
            return {"sub": parts[0], "token": token}
        return None
