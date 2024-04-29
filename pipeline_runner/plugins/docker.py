"""Docker plugin for building images and running containers."""

import logging
import subprocess
from pipeline_runner.plugins.base import PluginBase

logger = logging.getLogger(__name__)


class DockerPlugin(PluginBase):
    name = "docker"

    def __init__(self):
        super().__init__()
        self._containers: list[str] = []

    def build_image(self, tag: str, dockerfile: str = "Dockerfile") -> bool:
        # BUG: missing context directory argument — docker build fails without
        # knowing where to find the Dockerfile and build context.
        cmd = ["docker", "build", "-t", tag, "-f", dockerfile]
        logger.info("Building image: %s", " ".join(cmd))
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            logger.error("Build failed: %s", result.stderr)
            return False
        return True

    def run_container(self, image: str, name: str, env: dict | None = None) -> str:
        cmd = ["docker", "run", "-d", "--name", name]
        for key, val in (env or {}).items():
            cmd.extend(["-e", f"{key}={val}"])
        cmd.append(image)
        result = subprocess.run(cmd, capture_output=True, text=True)
        container_id = result.stdout.strip()
        self._containers.append(container_id)
        logger.info("Started container %s (%s)", name, container_id[:12])
        return container_id

    def cleanup_container(self, container_id: str) -> bool:
        subprocess.run(["docker", "rm", "-f", container_id], capture_output=True)
        self._containers = [c for c in self._containers if c != container_id]
        return True

    def execute(self, **kwargs) -> dict:
        action = kwargs.get("action", "build")
        if action == "build":
            ok = self.build_image(kwargs["tag"], kwargs.get("dockerfile", "Dockerfile"))
            return {"success": ok}
        elif action == "run":
            cid = self.run_container(kwargs["image"], kwargs["name"], kwargs.get("env"))
            return {"container_id": cid}
        return {"error": f"Unknown action: {action}"}
