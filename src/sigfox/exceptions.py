"""Custom exceptions for Sigfox API client."""


class SigfoxError(Exception):
    """Base exception for Sigfox API operations."""


class AuthenticationError(SigfoxError):
    """Authentication error (401)."""


class AuthorizationError(SigfoxError):
    """Authorization error (403)."""


class NotFoundError(SigfoxError):
    """Resource not found error (404)."""


class APIError(SigfoxError):
    """Sigfox API error."""

    def __init__(self, message: str, status_code: int | None = None, response_body: str | None = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body


class NetworkError(SigfoxError):
    """Network connection error."""


class ValidationError(SigfoxError):
    """Input validation error."""
