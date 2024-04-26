"""Abstract base class for all pipeline plugins."""

import logging
from abc import ABC, abstractmethod
from typing import Any

logger = logging.getLogger(__name__)


class PluginBase(ABC):
    name: str = "base"

    def __init__(self):
        self._initialized = False
        self._config: dict[str, Any] = {}
        logger.debug("Plugin '%s' instantiated", self.name)

    def configure(self, config: dict[str, Any]):
        self._config = config
        self._initialized = True
        logger.info("Plugin '%s' configured with %d keys", self.name, len(config))

    @abstractmethod
    def execute(self, **kwargs) -> dict:
        raise NotImplementedError

    @property
    def is_ready(self) -> bool:
        return self._initialized

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name={self.name!r} ready={self.is_ready}>"
