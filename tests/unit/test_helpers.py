"""Tests for formatting helper utilities."""
from pipeline_runner.utils.formatting import (
    format_duration,
    format_bytes,
    truncate_string,
)


class TestFormatDuration:
    def test_seconds(self):
        assert format_duration(30.5) == "30.5s"

    def test_minutes(self):
        assert format_duration(125) == "2m 5s"

    def test_hours(self):
        assert format_duration(3725) == "1h 2m 5s"


class TestFormatBytes:
    def test_bytes(self):
        assert format_bytes(500) == "500.0 B"

    def test_kilobytes(self):
        assert "KB" in format_bytes(2048)


class TestTruncateString:
    def test_short_string_unchanged(self):
        assert truncate_string("hello", max_len=10) == "hello"

    def test_long_string_truncated(self):
        result = truncate_string("a" * 100, max_len=10)
        assert len(result) == 10
        assert result.endswith("...")

    def test_max_len_smaller_than_suffix(self):
        result = truncate_string("a" * 100, max_len=2)
        assert len(result) <= 2
