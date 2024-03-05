"""Structured logging utilities."""
import json
import logging
from datetime import datetime


class StructuredFormatter(logging.Formatter):
    """Format log records as JSON."""

    def format(self, record):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        if hasattr(record, "extra_data"):
            log_entry["data"] = record.extra_data
        return json.dumps(log_entry)


def configure_logging(level=logging.INFO, structured=True):
    """Configure application logging."""
    root = logging.getLogger()
    root.setLevel(level)

    handler = logging.StreamHandler()
    if structured:
        handler.setFormatter(StructuredFormatter())
    else:
        handler.setFormatter(
            logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
        )

    root.handlers = [handler]
    return root


def get_logger(name):
    """Get a named logger instance."""
    return logging.getLogger(f"pipeline_runner.{name}")
