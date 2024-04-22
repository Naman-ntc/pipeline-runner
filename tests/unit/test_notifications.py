import pytest
from unittest.mock import MagicMock, patch
from notifications.email import EmailNotifier
from notifications.slack import SlackNotifier
from notifications.webhook import WebhookDispatcher
from notifications.dispatcher import NotificationDispatcher


class TestEmailNotifier:
    def test_validate_valid_email(self):
        notifier = EmailNotifier("smtp.test.com", 587, "noreply@test.com")
        assert notifier.validate_recipient("user@example.com") is True

    def test_validate_invalid_email(self):
        notifier = EmailNotifier("smtp.test.com", 587, "noreply@test.com")
        assert notifier.validate_recipient("not-an-email") is False

    def test_build_template_plain(self):
        notifier = EmailNotifier("smtp.test.com", 587, "noreply@test.com")
        msg = notifier.build_template("Subject", "Body text")
        assert msg["Subject"] == "Subject"
        assert msg["From"] == "noreply@test.com"

    def test_send_rejects_invalid(self):
        notifier = EmailNotifier("smtp.test.com", 587, "noreply@test.com")
        with pytest.raises(ValueError):
            notifier.send("bad-email", "Hi", "Body")


class TestSlackNotifier:
    def test_format_success(self):
        notifier = SlackNotifier("https://hooks.slack.com/test")
        result = notifier.format_pipeline_status("deploy", "success")
        assert result["attachments"][0]["color"] == "#36a64f"

    def test_format_failure(self):
        notifier = SlackNotifier("https://hooks.slack.com/test")
        result = notifier.format_pipeline_status("build", "failure", "timeout")
        assert "timeout" in result["attachments"][0]["text"]


class TestWebhookDispatcher:
    def test_register_url(self):
        wh = WebhookDispatcher(secret="s3cret")
        wh.register_url("https://example.com/hook")
        assert len(wh._urls) == 1

    def test_register_duplicate(self):
        wh = WebhookDispatcher(secret="s3cret")
        wh.register_url("https://example.com/hook")
        wh.register_url("https://example.com/hook")
        assert len(wh._urls) == 1

    def test_unregister_url(self):
        wh = WebhookDispatcher(secret="s3cret")
        wh.register_url("https://a.com")
        wh.register_url("https://b.com")
        wh.unregister_url("https://a.com")
        assert len(wh._urls) == 1

    def test_verify_signature_valid(self):
        import hmac, hashlib
        wh = WebhookDispatcher(secret="key")
        payload = b'{"event": "test"}'
        sig = hmac.new(b"key", payload, hashlib.sha256).hexdigest()
        assert wh.verify_signature(payload, sig) is True

    def test_verify_signature_invalid(self):
        wh = WebhookDispatcher(secret="key")
        assert wh.verify_signature(b"payload", "badsig") is False


class TestNotificationDispatcher:
    def test_dispatch_routes_to_channels(self):
        ch = MagicMock()
        ch.send.return_value = True
        dispatcher = NotificationDispatcher()
        dispatcher.add_channel("email", ch)
        dispatcher.route("deploy", ["email"])
        results = dispatcher.dispatch("deploy", "deployed v1.2")
        assert results["email"] is True
        ch.send.assert_called_once_with("deployed v1.2")

    def test_dispatch_handles_failure(self):
        ch = MagicMock()
        ch.send.side_effect = RuntimeError("boom")
        dispatcher = NotificationDispatcher()
        dispatcher.add_channel("slack", ch)
        dispatcher.route("error", ["slack"])
        results = dispatcher.dispatch("error", "something broke")
        assert results["slack"] is False

    def test_list_channels(self):
        dispatcher = NotificationDispatcher()
        dispatcher.add_channel("a", MagicMock())
        dispatcher.add_channel("b", MagicMock())
        assert sorted(dispatcher.list_channels()) == ["a", "b"]
