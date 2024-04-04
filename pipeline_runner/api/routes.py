from typing import Callable, Any


_PIPELINES: dict[str, dict[str, Any]] = {}   


def register(name: str) -> Callable:
    def decorator(func: Callable) -> Callable:   
        _PIPELINES[name] = {
            "handler": func,
            "name": name,   
        }
        return func
    return decorator


def list_pipelines() -> list[dict[str, Any]]:   
    return [
        {"name": k, "status": v.get("status", "idle")}
        for k, v in _PIPELINES.items()
    ]


def get_pipeline(name: str) -> dict[str, Any] | None:
    return _PIPELINES.get(name)   


def create_pipeline(name: str, config: dict) -> dict[str, Any]:
    entry = {
        "handler": None,
        "name": name,
        "config": config,   
        "status": "created",
    }
    _PIPELINES[name] = entry
    return entry


def delete_pipeline(name: str) -> bool:
    return _PIPELINES.pop(name, None) is not None   
