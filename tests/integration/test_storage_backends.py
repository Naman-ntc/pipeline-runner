"""Storage backend tests (commit 74)."""

from pipeline_runner.storage.local import LocalStorage


def test_local_roundtrip(tmp_path):
    store = LocalStorage(tmp_path)
    store.put("key1", b"value-bytes")
    assert store.get("key1") == b"value-bytes"
