"""Unit tests for the CLI main module."""

import pytest
from unittest.mock import patch
from cli.main import create_parser, dispatch_command


def test_create_parser_has_subcommands():
    parser = create_parser()
    assert parser.prog == "pipeline"
    args = parser.parse_args(["run", "my_pipeline"])
    assert args.pipeline_name == "my_pipeline"
    assert hasattr(args, "func")


def test_dispatch_command_calls_func():
    parser = create_parser()
    args = parser.parse_args(["config", "show"])
    with patch("builtins.print") as mock_print:
        dispatch_command(args)
        mock_print.assert_called_once()


def test_dispatch_no_subcommand_exits():
    parser = create_parser()
    args = parser.parse_args([])
    with pytest.raises(SystemExit):
        dispatch_command(args)


def test_config_path_default():
    parser = create_parser()
    args = parser.parse_args(["run", "etl", "--config", "/etc/pipeline.yaml"])
    assert args.config_path == "/etc/pipeline.yaml"
