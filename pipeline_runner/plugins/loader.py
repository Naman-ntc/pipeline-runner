"""Plugin loader that discovers and manages plugins from a directory."""

import importlib.util
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class PluginLoader:
    def __init__(self, plugin_dir: str):
        self.plugin_dir = Path(plugin_dir)
        self._plugins: dict[str, Any] = {}

    def discover(self) -> list[str]:
        if not self.plugin_dir.is_dir():
            logger.warning("Plugin directory not found: %s", self.plugin_dir)
            return []
        # BUG: includes __init__.py and other dunder files, which causes
        # load errors when they're treated as standalone plugins.
        found = [p.stem for p in self.plugin_dir.glob("*.py")]
        logger.info("Discovered %d plugin candidates: %s", len(found), found)
        return found

    def load(self, plugin_name: str) -> Any:
        path = self.plugin_dir / f"{plugin_name}.py"
        if not path.exists():
            raise FileNotFoundError(f"Plugin not found: {path}")
        spec = importlib.util.spec_from_file_location(plugin_name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self._plugins[plugin_name] = module
        logger.info("Loaded plugin: %s", plugin_name)
        return module

    def unload(self, plugin_name: str) -> bool:
        if plugin_name in self._plugins:
            del self._plugins[plugin_name]
            logger.info("Unloaded plugin: %s", plugin_name)
            return True
        return False

    def list_plugins(self) -> list[str]:
        return list(self._plugins.keys())
