"""Abstract base class for storage backends."""

from abc import ABC, abstractmethod
from typing import Iterator


class StorageBackend(ABC):
    """Interface that all storage backends must implement."""

    @abstractmethod
    def get(self, key: str):
        """Retrieve raw bytes for the given key."""
        ...

    @abstractmethod
    def put(self, key: str, content: bytes):
        """Store raw bytes under the given key."""
        ...

    @abstractmethod
    def delete(self, key: str):
        """Remove the object identified by *key*."""
        ...

    @abstractmethod
    def list_keys(self, prefix: str = ""):
        """Yield all keys that start with *prefix*."""
        ...

    @abstractmethod
    def exists(self, key: str):
        """Return True if *key* exists in the backend."""
        ...
