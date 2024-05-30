"""Health check utilities."""
import enum
from typing import Callable, Dict, List, Tuple


class HealthStatus(enum.Enum):
    """Possible health states for the system."""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


class HealthChecker:
    """Manages and runs health checks."""

    def __init__(self) -> None:
        self._checks: Dict[str, Callable[[], bool]] = {}

    def add_check(self, name: str, check_fn: Callable[[], bool]) -> None:
        """Register a named health check."""
        self._checks[name] = check_fn

    def run_checks(self) -> Tuple[HealthStatus, List[str]]:
        """Execute all checks and return overall status with failures."""
        failures: List[str] = []
        for name, check_fn in self._checks.items():
            try:
                if not check_fn():
                    failures.append(name)
            except Exception:
                failures.append(f"{name} (error)")

        if not failures:
            return HealthStatus.HEALTHY, []
        if len(failures) < len(self._checks):
            return HealthStatus.DEGRADED, failures
        return HealthStatus.UNHEALTHY, failures

    def is_healthy(self) -> bool:
        """Quick check returning True only if all checks pass."""
        status, _ = self.run_checks()
        return status == HealthStatus.HEALTHY
