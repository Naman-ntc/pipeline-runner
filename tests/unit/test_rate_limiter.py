import time
from unittest.mock import patch
from api.rate_limiter import RateLimiter


def test_allows_requests_under_limit():
    limiter = RateLimiter(max_requests=5, window_seconds=60)
    for _ in range(5):
        assert limiter.check("user1") is True


def test_blocks_over_limit():
    limiter = RateLimiter(max_requests=3, window_seconds=60)
    for _ in range(3):
        limiter.check("user1")
    assert limiter.check("user1") is False


def test_separate_keys_independent():
    limiter = RateLimiter(max_requests=2, window_seconds=60)
    limiter.check("a")
    limiter.check("a")
    assert limiter.check("a") is False
    assert limiter.check("b") is True


def test_reset_clears_key():
    limiter = RateLimiter(max_requests=1, window_seconds=60)
    limiter.check("user1")
    assert limiter.check("user1") is False
    limiter.reset("user1")
    assert limiter.check("user1") is True


def test_remaining_count():
    limiter = RateLimiter(max_requests=5, window_seconds=60)
    assert limiter.remaining("user1") == 5
    limiter.check("user1")
    limiter.check("user1")
    assert limiter.remaining("user1") == 3


def test_window_expiry():
    limiter = RateLimiter(max_requests=1, window_seconds=10)
    with patch("time.time", return_value=1000.0):
        assert limiter.check("user1") is True
    with patch("time.time", return_value=1011.0):
        assert limiter.check("user1") is True


def test_reset_nonexistent_key():
    limiter = RateLimiter(max_requests=5, window_seconds=60)
    limiter.reset("nonexistent")
    assert limiter.remaining("nonexistent") == 5
