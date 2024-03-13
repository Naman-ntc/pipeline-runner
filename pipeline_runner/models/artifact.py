from __future__ import annotations

import hashlib
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Artifact:
    """Binary produced by a pipeline run, identified by path and content hash."""

    id: str
    pipeline_id: str
    path: str
    size_bytes: int
    checksum: str = field(metadata={"algo": "sha256"})

    def validate_checksum(self, data: bytes) -> bool:
        digest = hashlib.sha256(data).hexdigest()
        return digest == self.checksum

    def size_mb(self) -> float:
        return self.size_bytes / (1024 * 1024)
