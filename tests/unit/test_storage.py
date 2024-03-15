"""Unit tests for LocalStorage and S3Storage."""

import pytest

from pipeline_runner.storage.local import LocalStorage
from pipeline_runner.storage.s3 import S3Storage


class TestLocalStorage:
    def test_put_and_get(self, tmp_path):
        store = LocalStorage(tmp_path / "data")
        store.put("greeting.txt", b"hello world")
        assert store.get("greeting.txt") == b"hello world"

    def test_put_nested_key(self, tmp_path):
        store = LocalStorage(tmp_path / "data")
        store.put("subdir/nested/file.bin", b"\x00\x01\x02")
        assert store.get("subdir/nested/file.bin") == b"\x00\x01\x02"

    def test_exists(self, tmp_path):
        store = LocalStorage(tmp_path / "data")
        assert not store.exists("missing.txt")
        store.put("missing.txt", b"data")
        assert store.exists("missing.txt")

    def test_delete(self, tmp_path):
        store = LocalStorage(tmp_path / "data")
        store.put("temp.txt", b"temp")
        store.delete("temp.txt")
        assert not store.exists("temp.txt")

    def test_list_keys(self, tmp_path):
        store = LocalStorage(tmp_path / "data")
        store.put("a.txt", b"a")
        store.put("b.txt", b"b")
        keys = sorted(store.list_keys())
        assert keys == ["a.txt", "b.txt"]

    def test_get_missing_raises(self, tmp_path):
        store = LocalStorage(tmp_path / "data")
        with pytest.raises(FileNotFoundError):
            store.get("no-such-key")


class TestS3StorageInit:
    def test_prefix_trailing_slash_stripped(self):
        store = S3Storage(bucket="my-bucket", prefix="data/")
        assert store.prefix == "data"

    def test_build_key_no_double_slash(self):
        store = S3Storage(bucket="my-bucket", prefix="data/")
        assert store._build_key("file.txt") == "data/file.txt"
