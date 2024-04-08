"""Request authentication decorators."""
from __future__ import annotations


def require_auth(fn):
    """Mark a handler as requiring authentication."""
    fn._requires_auth = True
    return fn
