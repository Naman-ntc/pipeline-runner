"""Heartbeat emitter that periodically reports worker health."""

import logging
import threading
import time
from typing import Callable

logger = logging.getLogger(__name__)


class HeartbeatEmitter:
    def __init__(self, interval: float, callback: Callable[[], dict]):
        self.interval = interval
        self.callback = callback
        self._running = False
        self._thread: threading.Thread | None = None
        self._last_health: dict | None = None

    def start(self):
        if self._running:
            logger.warning("Heartbeat emitter already running")
            return
        self._running = True
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        logger.info("Heartbeat emitter started with interval=%.1fs", self.interval)

    def stop(self):
        self._running = False
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=self.interval * 2)
        self._thread = None
        logger.info("Heartbeat emitter stopped")

    def emit(self) -> dict:
        health = self.callback()
        self._last_health = health
        logger.debug("Heartbeat emitted: %s", health)
        return health

    def check_health(self) -> dict | None:
        return self._last_health

    def _run_loop(self):
        while self._running:
            try:
                self.emit()
            except Exception as exc:
                logger.error("Heartbeat emission failed: %s", exc)
            # BUG: always sleeps the full interval regardless of how long emit() took,
            # causing the actual period to drift longer than self.interval.
            time.sleep(self.interval)
