import time
from unittest.mock import patch
from auth.tokens import generate_token, verify_token, revoke_token, is_revoked, _TOKEN_STORE, _REVOKED


def setup_function():
    _TOKEN_STORE.clear()
    _REVOKED.clear()


def test_generate_token_returns_pair():
    token, payload = generate_token("user123")
    assert "." in token
    assert payload.sub == "user123"
    assert payload.exp > payload.iat


def test_generate_token_custom_ttl():
    token, payload = generate_token("user1", ttl_seconds=7200)
    assert payload.exp - payload.iat == pytest.approx(7200, abs=1)


def test_verify_valid_token():
    token, payload = generate_token("user1")
    result = verify_token(token)
    assert result is not None
    assert result.sub == "user1"


def test_verify_invalid_format():
    assert verify_token("no-dot-here") is None
    assert verify_token("") is None


def test_verify_unknown_token():
    assert verify_token("unknown.signature") is None


def test_revoke_token_makes_verify_fail():
    token, _ = generate_token("user1")
    revoke_token(token)
    assert verify_token(token) is None


def test_is_revoked():
    token, _ = generate_token("user1")
    assert is_revoked(token) is False
    revoke_token(token)
    assert is_revoked(token) is True


def test_verify_expired_token():
    with patch("time.time", return_value=1000.0):
        token, _ = generate_token("user1", ttl_seconds=60)
    with patch("time.time", return_value=1061.0):
        result = verify_token(token)
        assert result is None


import pytest
