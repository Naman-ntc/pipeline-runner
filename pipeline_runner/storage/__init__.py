"""Pluggable storage backends for the application."""

from pipeline_runner.storage.local import LocalStorage
from pipeline_runner.storage.s3 import S3Storage

__all__ = ["LocalStorage", "S3Storage"]
