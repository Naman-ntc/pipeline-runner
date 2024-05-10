import hashlib
import hmac
import json
import urllib.request
from typing import Any


class WebhookDispatcher:
    def __init__(self, secret: str) -> None:
        self.secret = secret
        self._urls: list[str] = []

    def register_url(self, url: str) -> None:
        if url not in self._urls:
            self._urls.append(url)

    def unregister_url(self, url: str) -> None:
        self._urls = [u for u in self._urls if u != url]

    def verify_signature(self, payload: bytes, signature: str) -> bool:
        expected = hmac.new(
            self.secret.encode(), payload, hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(signature, expected)

    def dispatch(self, event: str, data: dict[str, Any]) -> list[dict]:
        body = json.dumps({"event": event, "data": data}).encode()
        sig = hmac.new(self.secret.encode(), body, hashlib.sha256).hexdigest()
        results = []
        for url in self._urls:
            req = urllib.request.Request(
                url,
                data=body,
                headers={
                    "Content-Type": "application/json",
                    "X-Signature": sig,
                },
            )
            try:
                resp = urllib.request.urlopen(req)
                results.append({"url": url, "status": resp.status})
            except Exception as exc:
                results.append({"url": url, "error": str(exc)})
        return results
