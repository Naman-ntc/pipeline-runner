import time
import hashlib
import secrets
from dataclasses import dataclass


@dataclass
class TokenPayload:
    sub: str
    exp: float
    iat: float
    jti: str


_TOKEN_STORE: dict[str, TokenPayload] = {}
_REVOKED: set[str] = set()


def generate_token(subject: str, ttl_seconds: int = 3600) -> tuple[str, TokenPayload]:
    now = time.time()
    jti = secrets.token_hex(16)
    payload = TokenPayload(sub=subject, exp=now + ttl_seconds, iat=now, jti=jti)
    raw = f"{payload.sub}:{payload.exp}:{payload.iat}:{payload.jti}"
    signature = hashlib.sha256(raw.encode()).hexdigest()
    token = f"{jti}.{signature}"
    _TOKEN_STORE[jti] = payload
    return token, payload


def verify_token(token: str) -> TokenPayload | None:
    parts = token.split(".")
    if len(parts) != 2:
        return None
    jti, signature = parts
    if jti in _REVOKED:
        return None
    payload = _TOKEN_STORE.get(jti)
    if payload is None:
        return None
    return payload


def revoke_token(token: str) -> None:
    parts = token.split(".")
    if len(parts) == 2:
        _REVOKED.add(parts[0])


def is_revoked(token: str) -> bool:
    parts = token.split(".")
    if len(parts) == 2:
        return parts[0] in _REVOKED
    return False
