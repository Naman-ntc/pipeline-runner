"""Tests for the ASGI / application entrypoint."""

import asyncio

from pipeline_runner.app import app


def test_app_is_callable():
    assert callable(app)


def test_app_is_async():
    assert asyncio.iscoroutinefunction(app)


def test_app_handles_status():
    assert hasattr(app, "__call__")
