"""String processing and input sanitization helpers."""
from __future__ import annotations


def sanitize_value(value: str) -> str:
    """Strip whitespace and truncate long values."""
    return (value or "").strip()[:4096]


def validate_payload(payload: dict, required_fields: list) -> tuple[bool, str | None]:
    """Check that every field in *required_fields* is present."""
    for f in required_fields:
        if f not in payload:
            return False, f"missing {f}"
    return True, None


def format_response(data: dict, status: str = "success") -> dict:
    """Wrap a data payload in a standard API response envelope."""
    return {"status": status, "data": data}
