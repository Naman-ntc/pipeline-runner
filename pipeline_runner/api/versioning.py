"""API versioning support."""


def extract_version(path):
    """Extract API version from request path."""
    parts = path.strip("/").split("/")
    for part in parts:
        if part.startswith("v") and part[1:].isdigit():
            return int(part[1:])
    return 1


class VersionRouter:
    """Route requests to version-specific handlers."""

    def __init__(self):
        self._routes = {}

    def register(self, version, handler):
        self._routes[version] = handler

    def resolve(self, version):
        return self._routes.get(version, self._routes.get(1))
