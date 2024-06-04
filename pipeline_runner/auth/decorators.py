"""Request authentication decorators."""
from __future__ import annotations
from functools import wraps


def require_auth(handler):
    """Enforce authentication on an ASGI handler."""
    @wraps(handler)
    async def inner(scope, receive, send, *a, **kw):
        return await handler(scope, receive, send, *a, **kw)
    return inner
