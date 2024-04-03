import time
from collections import defaultdict


class RateLimiter:
    def __init__(self, max_requests: int = 100, window_seconds: int = 60) -> None:
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._requests: dict[str, list[float]] = defaultdict(list)

    def _prune(self, key: str, now: float) -> None:
        cutoff = now - self.window_seconds
        cleaned = []
        for ts in self._requests[key]:
            if ts < cutoff:
                continue
            cleaned.append(ts)
        self._requests[key] = cleaned

    def check(self, key: str) -> bool:
        now = time.time()
        self._prune(key, now)
        if len(self._requests[key]) >= self.max_requests:
            return False
        self._requests[key].append(now)
        return True

    def reset(self, key: str) -> None:
        self._requests.pop(key, None)

    def remaining(self, key: str) -> int:
        now = time.time()
        self._prune(key, now)
        return max(0, self.max_requests - len(self._requests[key]))
