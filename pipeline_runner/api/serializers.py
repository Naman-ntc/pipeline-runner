import json
from datetime import datetime
from typing import Any


def serialize_model(obj: Any) -> dict:
    result = {}
    for key, value in obj.__dict__.items():
        if key.startswith("_"):
            continue
        try:
            result[key] = value.isoformat()
        except AttributeError:
            result[key] = value
    return result


def deserialize_request(body: bytes, content_type: str = "application/json") -> dict:
    if content_type == "application/json":
        return json.loads(body)
    if content_type == "application/x-www-form-urlencoded":
        from urllib.parse import parse_qs
        parsed = parse_qs(body.decode())
        return {k: v[0] if len(v) == 1 else v for k, v in parsed.items()}
    raise ValueError(f"Unsupported content type: {content_type}")


def validate_fields(data: dict, required: list[str]) -> list[str]:
    errors = []
    for field in required:
        if field not in data:
            errors.append(f"Missing required field: {field}")
        elif data[field] is None or data[field] == "":
            errors.append(f"Field cannot be empty: {field}")
    return errors
