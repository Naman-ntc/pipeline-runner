"""AWS S3 storage backend with lazy client initialisation."""

from __future__ import annotations

from typing import Iterator, Optional

from pipeline_runner.storage.base import StorageBackend


class S3Storage(StorageBackend):
    """Store objects in an S3 bucket under an optional prefix."""

    def __init__(
        self,
        bucket: str,
        prefix: str = "",
        region: Optional[str] = None,
    ) -> None:
        self.bucket = bucket
        self.prefix = prefix.rstrip("/")
        self.region = region
        self._client = None

    def _get_client(self):
        if self._client is None:
            import boto3
            kwargs = {}
            if self.region:
                kwargs["region_name"] = self.region
            self._client = boto3.client("s3", **kwargs)
        return self._client

    def _build_key(self, key: str) -> str:
        if self.prefix:
            return f"{self.prefix}/{key}"
        return key

    def get(self, key: str) -> bytes:
        from botocore.exceptions import ClientError
        client = self._get_client()
        try:
            resp = client.get_object(Bucket=self.bucket, Key=self._build_key(key))
            return resp["Body"].read()
        except ClientError as exc:
            if exc.response["Error"]["Code"] == "NoSuchKey":
                raise FileNotFoundError(f"Key not found: {key}") from exc
            raise

    def put(self, key: str, content: bytes) -> None:
        client = self._get_client()
        client.put_object(Bucket=self.bucket, Key=self._build_key(key), Body=content)

    def delete(self, key: str) -> None:
        client = self._get_client()
        client.delete_object(Bucket=self.bucket, Key=self._build_key(key))

    def list_keys(self, prefix: str = "") -> Iterator[str]:
        client = self._get_client()
        full_prefix = self._build_key(prefix)
        paginator = client.get_paginator("list_objects_v2")
        for page in paginator.paginate(Bucket=self.bucket, Prefix=full_prefix):
            for obj in page.get("Contents", []):
                raw_key = obj["Key"]
                if self.prefix:
                    raw_key = raw_key[len(self.prefix) + 1 :]
                yield raw_key

    def exists(self, key: str) -> bool:
        from botocore.exceptions import ClientError
        client = self._get_client()
        try:
            client.head_object(Bucket=self.bucket, Key=self._build_key(key))
            return True
        except ClientError:
            return False
