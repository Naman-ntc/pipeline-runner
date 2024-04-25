"""CLI command tests (commit 89)."""

from cli.commands.run import handle_run


def test_handle_run_exists():
    assert callable(handle_run)
