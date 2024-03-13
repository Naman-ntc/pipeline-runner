from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Environment:
    """Deployment environment with variables and references to external secrets."""

    name: str
    variables: dict[str, str] = field(default_factory=dict)
    secrets_ref: list[str] = field(default_factory=list)
    region: str = "us-east-1"

    def merge_variables(self, other: dict[str, str]) -> None:
        """Overlay keys from other into variables (later keys win on conflict)."""
        self.variables.update(other)

    def has_secrets(self) -> bool:
        return bool(self.secrets_ref)

    def variable_count(self) -> int:
        return len(self.variables)
