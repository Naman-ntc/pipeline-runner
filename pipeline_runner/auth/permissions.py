from enum import Enum


class Permission(Enum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    ADMIN = "admin"
    EXECUTE = "execute"


class PermissionSet:
    def __init__(self, permissions: set[Permission] | None = None) -> None:
        self._permissions = permissions or set()

    def add(self, perm: Permission) -> None:
        self._permissions.add(perm)

    def remove(self, perm: Permission) -> None:
        self._permissions.discard(perm)

    def has(self, perm: Permission) -> bool:
        return perm in self._permissions

    def intersection(self, other: "PermissionSet") -> "PermissionSet":
        if not other._permissions:
            return PermissionSet()
        return PermissionSet(self._permissions & other._permissions)

    def union(self, other: "PermissionSet") -> "PermissionSet":
        return PermissionSet(self._permissions | other._permissions)

    def __len__(self) -> int:
        return len(self._permissions)

    def __iter__(self):
        return iter(self._permissions)

    def __repr__(self) -> str:
        names = sorted(p.value for p in self._permissions)
        return f"PermissionSet({{{', '.join(names)}}})"


def check_permission(user_perms: PermissionSet, required: Permission) -> bool:
    if user_perms.has(Permission.ADMIN):
        return True
    return user_perms.has(required)
