"""Shell plugin for executing system commands."""

import logging
import os
import subprocess
from pipeline_runner.plugins.base import PluginBase

logger = logging.getLogger(__name__)


class ShellPlugin(PluginBase):
    name = "shell"

    def __init__(self):
        super().__init__()
        self._env: dict[str, str] = dict(os.environ)

    def set_env(self, key: str, value: str):
        self._env[key] = value
        logger.debug("Set env %s=%s", key, value[:20])

    def run_command(self, cmd: list[str], cwd: str | None = None) -> int:
        logger.info("Running command: %s", " ".join(cmd))
        result = subprocess.run(cmd, cwd=cwd, env=self._env,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            logger.error("Command failed (exit %d): %s", result.returncode, result.stderr)
        return result.returncode

    def capture_output(self, cmd: list[str], cwd: str | None = None) -> tuple[str, str, int]:
        result = subprocess.run(cmd, cwd=cwd, env=self._env,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout, result.stderr, result.returncode

    def execute(self, **kwargs) -> dict:
        cmd = kwargs.get("command", [])
        if isinstance(cmd, str):
            cmd = cmd.split()
        stdout, stderr, code = self.capture_output(cmd, kwargs.get("cwd"))
        return {"stdout": stdout, "stderr": stderr, "exit_code": code}
