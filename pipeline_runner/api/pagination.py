from dataclasses import dataclass
from typing import Any


@dataclass
class PaginationParams:
    limit: int = 20
    offset: int = 0

    def __post_init__(self):
        self.limit = max(1, min(self.limit, 100))
        self.offset = max(0, self.offset)


def paginate(items: Any, limit: int = 20, offset: int = 0) -> list:
    materialized = list(items)
    return materialized[offset:offset + limit]


def build_page_response(
    items: list,
    total: int,
    limit: int,
    offset: int,
) -> dict:
    has_next = offset + limit < total
    has_prev = offset > 0
    return {
        "data": items,
        "pagination": {
            "total": total,
            "limit": limit,
            "offset": offset,
            "has_next": has_next,
            "has_prev": has_prev,
            "next_offset": offset + limit if has_next else None,
            "prev_offset": max(0, offset - limit) if has_prev else None,
        },
    }
