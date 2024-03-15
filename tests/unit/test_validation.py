"""Tests for validation utilities."""
import pytest

from pipeline_runner.utils.validation import (
    validate_email,
    validate_url,
    validate_cron,
    validate_identifier,
)


class TestValidateEmail:
    def test_valid_email(self):
        assert validate_email("user@example.com") is True

    def test_invalid_email_no_at(self):
        assert validate_email("userexample.com") is False

    def test_rejects_missing_dot_in_domain(self):
        assert validate_email("user@exampleXcom") is False

    def test_rejects_empty(self):
        assert validate_email("") is False


class TestValidateUrl:
    def test_valid_url(self):
        assert validate_url("https://example.com/path") is True

    def test_invalid_url(self):
        assert validate_url("not-a-url") is False


class TestValidateCron:
    def test_valid_cron(self):
        assert validate_cron("0 * * * *") is True

    def test_invalid_cron(self):
        assert validate_cron("invalid") is False
