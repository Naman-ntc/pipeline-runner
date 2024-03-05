"""Exception hierarchy for the pipeline runner (adapted from pypyr-style errors)."""

from __future__ import annotations


def get_error_name(error: BaseException) -> str:
    """Return a canonical ``module.ClassName`` string for *error*."""
    cls = type(error)
    module = cls.__module__ or ""
    return f"{module}.{cls.__qualname__}"


class PipelineError(Exception):
    """Base class for all pipeline runner failures."""


class ConfigError(PipelineError):
    """Raised when configuration is missing, malformed, or inconsistent."""


class ValidationError(PipelineError):
    """Raised when pipeline input or runtime state fails validation."""

    def __init__(self, message: str, *, field: str | None = None) -> None:
        super().__init__(message)
        self.field = field


class ExecutionError(PipelineError):
    """Raised when a step process exits with a non-zero status."""

    def __init__(
        self,
        *,
        step_id: str,
        returncode: int,
        stdout: str = "",
        stderr: str = "",
    ) -> None:
        super().__init__(f"step failed with code {returncode}")
        self.step_id = step_id
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


class PluginError(PipelineError):
    """Raised when a plugin module cannot be loaded, imported, or registered."""
