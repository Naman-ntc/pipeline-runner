"""Input validation utilities."""
import re
from typing import Optional


EMAIL_PATTERN = re.compile(
    r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,}$"
)

URL_PATTERN = re.compile(
    r"^https?://[^\s/$.?#].[^\s]*$"
)

CRON_PATTERN = re.compile(
    r"^(\*|[0-9,\-/]+)\s+(\*|[0-9,\-/]+)\s+(\*|[0-9,\-/]+)\s+"
    r"(\*|[0-9,\-/]+)\s+(\*|[0-9,\-/]+)$"
)


def validate_email(email: str) -> bool:
    """Validate an email address format."""
    if not email or len(email) > 254:
        return False
    return EMAIL_PATTERN.match(email) is not None


def validate_url(url: str) -> bool:
    """Validate a URL format."""
    if not url or len(url) > 2048:
        return False
    return URL_PATTERN.match(url) is not None


def validate_cron(expression: str) -> bool:
    """Validate a cron expression (5-field format)."""
    if not expression or not expression.strip():
        return False
    return CRON_PATTERN.match(expression.strip()) is not None


def validate_identifier(name: str, max_length: int = 128) -> Optional[str]:
    """Validate a pipeline identifier. Returns error message or None."""
    if not name:
        return "Identifier must not be empty"
    if len(name) > max_length:
        return f"Identifier exceeds max length of {max_length}"
    if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_\-]*$", name):
        return "Identifier contains invalid characters"
    return None
