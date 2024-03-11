"""Output formatting utilities."""
from datetime import datetime, timezone
from typing import Optional


def format_duration(seconds: float) -> str:
    """Format a duration in seconds to a human-readable string."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes, secs = divmod(int(seconds), 60)
    if minutes < 60:
        return f"{minutes}m {secs}s"
    hours, mins = divmod(minutes, 60)
    return f"{hours}h {mins}m {secs}s"


def format_bytes(num_bytes: int) -> str:
    """Format byte count to human-readable string."""
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if abs(num_bytes) < 1024:
            return f"{num_bytes:.1f} {unit}"
        num_bytes /= 1024
    return f"{num_bytes:.1f} PB"


def format_timestamp(
    dt: Optional[datetime] = None, fmt: str = "%Y-%m-%d %H:%M:%S UTC"
) -> str:
    """Format a datetime to string, defaulting to now in UTC."""
    if dt is None:
        dt = datetime.now(timezone.utc)
    return dt.strftime(fmt)


def truncate_string(text: str, max_len: int = 80, suffix: str = "...") -> str:
    """Truncate a string to max_len, adding suffix if truncated."""
    if len(text) <= max_len:
        return text
    return text[: max_len - len(suffix)] + suffix
