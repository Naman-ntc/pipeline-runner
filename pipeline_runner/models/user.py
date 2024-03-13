from __future__ import annotations

from dataclasses import dataclass, field

_ROLE_PERMISSIONS: dict[str, frozenset[str]] = {
    "admin": frozenset({"all"}),
    "developer": frozenset({"read", "write", "execute"}),
    "viewer": frozenset({"read"}),
}


@dataclass
class User:
    id: str
    username: str
    email: str
    role: str
    api_key: str = field(repr=False)

    def is_admin(self) -> bool:
        return self.role == "admin"

    def has_permission(self, perm: str) -> bool:
        allowed = _ROLE_PERMISSIONS.get(self.role, frozenset())
        if "all" in allowed:
            return True
        return perm in allowed
