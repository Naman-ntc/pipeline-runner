from pipeline_runner.app import app


def application(environ, start_response):
    start_response(
        "200 OK",
        [("Content-Type", "text/plain; charset=utf-8")],
    )
    return [b"Use ASGI server"]
