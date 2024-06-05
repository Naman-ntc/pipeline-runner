"""Tests for configuration loading."""

from pipeline_runner.config import AppConfig, get_config


def test_get_config_returns_appconfig():
    cfg = get_config()
    assert isinstance(cfg, AppConfig)


def test_config_has_from_env():
    assert hasattr(AppConfig, "from_env")
