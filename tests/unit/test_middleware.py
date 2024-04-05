import pytest
from api.middleware import LoggingMiddleware, CORSMiddleware, AuthMiddleware


async def echo_app(scope, receive, send):
    await send({
        "type": "http.response.start",
        "status": 200,
        "headers": [],
    })
    await send({"type": "http.response.body", "body": b"ok"})


def _make_send():
    captured = []

    async def send(msg):
        captured.append(msg)

    return send, captured


@pytest.mark.asyncio
async def test_cors_adds_origin_header():
    app = CORSMiddleware(echo_app, allowed_origins=["https://example.com"])
    send, captured = _make_send()
    scope = {"type": "http", "method": "GET", "path": "/"}
    await app(scope, None, send)
    start_msg = captured[0]
    header_dict = dict(start_msg["headers"])
    assert b"access-control-allow-origin" in header_dict


@pytest.mark.asyncio
async def test_cors_passthrough_non_http():
    app = CORSMiddleware(echo_app)
    send, captured = _make_send()
    scope = {"type": "websocket", "path": "/ws"}
    await app(scope, None, send)
    assert len(captured) == 2


@pytest.mark.asyncio
async def test_auth_no_token_sets_none():
    app = AuthMiddleware(echo_app, secret_key="secret")
    send, captured = _make_send()
    scope = {"type": "http", "method": "GET", "path": "/", "headers": []}
    await app(scope, None, send)
    assert scope["user"] is None


@pytest.mark.asyncio
async def test_auth_with_bearer_token():
    app = AuthMiddleware(echo_app, secret_key="secret")
    send, captured = _make_send()
    scope = {
        "type": "http",
        "method": "GET",
        "path": "/",
        "headers": [(b"authorization", b"Bearer abc.def")],
    }
    await app(scope, None, send)
    assert scope["user"] is not None
    assert scope["user"]["sub"] == "abc"


@pytest.mark.asyncio
async def test_logging_passthrough():
    app = LoggingMiddleware(echo_app)
    send, captured = _make_send()
    scope = {"type": "http", "method": "GET", "path": "/test"}
    await app(scope, None, send)
    assert len(captured) == 2
