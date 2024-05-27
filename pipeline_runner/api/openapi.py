from typing import Any


class SchemaBuilder:
    def __init__(self, title: str, version: str = "1.0.0") -> None:
        self.title = title
        self.version = version
        self._endpoints: list[dict[str, Any]] = []

    def register_endpoint(
        self,
        path: str,
        method: str,
        summary: str = "",
        request_body: dict | None = None,
        responses: dict | None = None,
    ) -> None:
        self._endpoints.append({
            "path": path,
            "method": method.lower(),
            "summary": summary,
            "requestBody": request_body,
            "responses": responses or {"200": {"description": "OK"}},
        })

    def generate_schema(self) -> dict:
        schema: dict[str, Any] = {
            "openapi": "3.0.3",
            "info": {
                "title": self.title,
                "version": self.version,
            },
        }
        paths: dict[str, Any] = {}
        for ep in self._endpoints:
            path = ep["path"]
            if path not in paths:
                paths[path] = {}
            operation: dict[str, Any] = {
                "summary": ep["summary"],
                "responses": ep["responses"],
            }
            if ep["requestBody"]:
                operation["requestBody"] = ep["requestBody"]
            paths[path][ep["method"]] = operation
        schema["paths"] = paths
        return schema
