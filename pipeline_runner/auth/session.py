import time
import secrets
from dataclasses import dataclass, field


@dataclass
class Session:
    session_id: str
    user_id: str
    data: dict = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
    expires_at: float = 0.0


class SessionStore:
    def __init__(self, default_ttl: int = 1800) -> None:
        self.default_ttl = default_ttl
        self._sessions: dict[str, Session] = {}

    def create(self, user_id: str, data: dict | None = None, ttl: int | None = None) -> Session:
        sid = secrets.token_urlsafe(32)
        ttl_val = ttl if ttl is not None else self.default_ttl
        now = time.time()
        session = Session(
            session_id=sid,
            user_id=user_id,
            data=data or {},
            created_at=now,
            expires_at=now + ttl_val,
        )
        self._sessions[sid] = session
        return session

    def get(self, session_id: str) -> Session | None:
        session = self._sessions.get(session_id)
        if session is None:
            return None
        if session.expires_at < time.time():
            self._sessions.pop(session_id, None)
            return None
        return session

    def destroy(self, session_id: str) -> bool:
        return self._sessions.pop(session_id, None) is not None

    def active_count(self) -> int:
        now = time.time()
        return sum(1 for s in self._sessions.values() if s.expires_at > now)
