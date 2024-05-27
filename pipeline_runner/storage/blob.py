"""Content-addressable blob store built on top of a StorageBackend."""

from __future__ import annotations

import hashlib
from typing import Optional, Union

from pipeline_runner.storage.base import StorageBackend


class BlobStore:
    """Stores data keyed by its SHA-256 content hash."""

    HASH_ALGO = "sha256"

    def __init__(self, backend: StorageBackend, prefix: str = "blobs") -> None:
        self.backend = backend
        self.prefix = prefix

    def compute_hash(self, data: Union[bytes, str]) -> str:
        """Return the hex digest for *data*."""
        if isinstance(data, str):
            data = data.encode()
        return hashlib.new(self.HASH_ALGO, data).hexdigest()

    def _blob_key(self, digest: str) -> str:
        return f"{self.prefix}/{digest[:2]}/{digest}"

    def store_blob(self, data: Union[bytes, str]) -> str:
        """Store *data* and return its content hash.

        If a blob with the same hash already exists the write is skipped.
        """
        if isinstance(data, str):
            data = data.encode()
        digest = self.compute_hash(data)
        key = self._blob_key(digest)
        if not self.backend.exists(key):
            self.backend.put(key, data)
        return digest

    def retrieve_blob(self, digest: str) -> bytes:
        """Fetch blob contents by hash. Raises FileNotFoundError if missing."""
        key = self._blob_key(digest)
        return self.backend.get(key)

    def blob_exists(self, digest: str) -> bool:
        key = self._blob_key(digest)
        return self.backend.exists(key)

    def delete_blob(self, digest: str) -> None:
        key = self._blob_key(digest)
        self.backend.delete(key)
