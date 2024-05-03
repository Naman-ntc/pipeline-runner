import json
import time
import urllib.request
import urllib.error


class SlackNotifier:
    def __init__(self, webhook_url: str, default_channel: str = "#general") -> None:
        self.webhook_url = webhook_url
        self.default_channel = default_channel

    def format_pipeline_status(self, name: str, status: str, details: str = "") -> dict:
        color_map = {
            "success": "#36a64f",
            "failure": "#ff0000",
            "running": "#ffaa00",
        }
        color = color_map.get(status, "#cccccc")
        return {
            "attachments": [
                {
                    "color": color,
                    "title": f"Pipeline: {name}",
                    "text": f"Status: {status}" + (f"\n{details}" if details else ""),
                    "fallback": f"{name}: {status}",
                }
            ]
        }

    def send_message(self, text: str, channel: str | None = None) -> bool:
        payload = {
            "channel": channel or self.default_channel,
            "text": text,
        }
        data = json.dumps(payload).encode()
        req = urllib.request.Request(
            self.webhook_url,
            data=data,
            headers={"Content-Type": "application/json"},
        )
        last_err: Exception | None = None
        for attempt in range(3):
            try:
                urllib.request.urlopen(req)
                return True
            except (urllib.error.URLError, OSError) as exc:
                last_err = exc
                time.sleep(2 ** attempt)
        raise ConnectionError(f"Failed after 3 attempts: {last_err}")
