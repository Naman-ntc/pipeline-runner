"""Tests for configuration loading."""

from pipeline_runner.config import get_config


def test_get_config_returns_dict():
    cfg = get_config()
    assert isinstance(cfg, dict)
    assert "service_name" in cfg


def test_config_has_required_keys():
    cfg = get_config()
    required = {
        "service_name",
        "environment",
        "log_level",
        "max_workers",
        "timeout_seconds",
    }
    assert required.issubset(cfg.keys())
