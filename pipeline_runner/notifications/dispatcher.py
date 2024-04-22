from typing import Any, Protocol


class NotificationChannel(Protocol):
    def send(self, *args: Any, **kwargs: Any) -> bool: ...


class NotificationDispatcher:
    def __init__(self) -> None:
        self._channels: dict[str, Any] = {}
        self._routes: dict[str, list[str]] = {}

    def add_channel(self, name: str, channel: Any) -> None:
        self._channels[name] = channel

    def route(self, event: str, channel_names: list[str]) -> None:
        self._routes[event] = channel_names

    def dispatch(self, event: str, message: str, **kwargs: Any) -> dict[str, bool]:
        channel_names = self._routes.get(event, [])
        results: dict[str, bool] = {}
        for name in channel_names:
            channel = self._channels.get(name)
            if channel is None:
                continue
            try:
                channel.send(message, **kwargs)
                results[name] = True
            except Exception:
                results[name] = False
        return results

    def list_channels(self) -> list[str]:
        return list(self._channels.keys())

    def list_routes(self) -> dict[str, list[str]]:
        return dict(self._routes)
