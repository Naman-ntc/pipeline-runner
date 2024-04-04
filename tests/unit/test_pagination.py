from api.pagination import PaginationParams, paginate, build_page_response


def test_pagination_params_defaults():
    params = PaginationParams()
    assert params.limit == 20
    assert params.offset == 0


def test_pagination_params_clamps_limit():
    params = PaginationParams(limit=200, offset=-5)
    assert params.limit == 100
    assert params.offset == 0


def test_pagination_params_minimum_limit():
    params = PaginationParams(limit=-10)
    assert params.limit == 1


def test_paginate_first_page():
    items = list(range(50))
    result = paginate(items, limit=10, offset=0)
    assert result == list(range(10))


def test_paginate_with_offset():
    items = list(range(50))
    result = paginate(items, limit=10, offset=20)
    assert result == list(range(20, 30))


def test_paginate_beyond_end():
    items = list(range(5))
    result = paginate(items, limit=10, offset=10)
    assert result == []


def test_build_page_response_first_page():
    resp = build_page_response(items=[1, 2, 3], total=30, limit=10, offset=0)
    assert resp["data"] == [1, 2, 3]
    assert resp["pagination"]["has_next"] is True
    assert resp["pagination"]["has_prev"] is False
    assert resp["pagination"]["next_offset"] == 10
    assert resp["pagination"]["prev_offset"] is None


def test_build_page_response_last_page():
    resp = build_page_response(items=[28, 29, 30], total=30, limit=10, offset=20)
    assert resp["pagination"]["has_next"] is False
    assert resp["pagination"]["has_prev"] is True
    assert resp["pagination"]["next_offset"] is None


def test_build_page_response_middle_page():
    resp = build_page_response(items=list(range(10)), total=50, limit=10, offset=10)
    assert resp["pagination"]["has_next"] is True
    assert resp["pagination"]["has_prev"] is True
    assert resp["pagination"]["next_offset"] == 20
    assert resp["pagination"]["prev_offset"] == 0
