"""String processing and input sanitization helpers."""
from __future__ import annotations


def sanitize_input(value: str) -> str:
    """Strip whitespace and truncate long input values."""
    return (value or "").strip()[:4096]


def format_response(data: dict, status: str = "success") -> dict:
    """Wrap a data payload in a standard API response envelope."""
    return {"status": status, "data": data}
