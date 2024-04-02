"""API error hierarchy."""


class APIError(Exception):
    """Base API error."""

    status_code = 500

    def __init__(self, message, status_code=None):
        super().__init__(message)
        if status_code is not None:
            self.status_code = status_code


class NotFoundError(APIError):
    """Resource not found."""

    status_code = 404


class AuthenticationError(APIError):
    """Authentication failed."""

    status_code = 401


def error_response(error):
    """Convert an APIError to a response dict."""
    return {
        "error": type(error).__name__,
        "message": str(error),
        "status_code": error.status_code if isinstance(error, APIError) else 500,
    }
