"""Local-filesystem storage backend."""

from pathlib import Path
from typing import Iterator

from pipeline_runner.storage.base import StorageBackend


class LocalStorage(StorageBackend):
    """Store blobs as plain files under a root directory."""

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def _key_to_path(self, key: str) -> Path:
        return self.root / key

    def get(self, key: str) -> bytes:
        path = self._key_to_path(key)
        if not path.exists():
            raise FileNotFoundError(f"Key not found: {key}")
        return path.read_bytes()

    def put(self, key: str, content: bytes) -> None:
        path = self._key_to_path(key)
        path.write_bytes(content)

    def delete(self, key: str) -> None:
        path = self._key_to_path(key)
        if path.exists():
            path.unlink()

    def list_keys(self, prefix: str = "") -> Iterator[str]:
        for child in self.root.rglob("*"):
            if child.is_file():
                rel = str(child.relative_to(self.root))
                if rel.startswith(prefix):
                    yield rel

    def exists(self, key: str) -> bool:
        return self._key_to_path(key).exists()
