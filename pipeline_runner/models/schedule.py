"""Schedule model for cron-based pipeline triggers."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Schedule:
    cron_expression: str
    pipeline_name: str
    enabled: bool = True
    last_run: Optional[datetime] = None

    def next_run(self) -> Optional[datetime]:
        try:
            from croniter import croniter
        except ImportError:
            return None
        base = self.last_run or datetime.now()
        it = croniter(self.cron_expression, base)
        return it.get_next(datetime)
