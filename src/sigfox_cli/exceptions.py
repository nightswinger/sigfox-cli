"""Custom exceptions for Sigfox CLI."""


class SigfoxCLIError(Exception):
    """Base exception for Sigfox CLI."""


class ConfigError(SigfoxCLIError):
    """Configuration error."""


class AuthenticationError(SigfoxCLIError):
    """Authentication error (401)."""


class AuthorizationError(SigfoxCLIError):
    """Authorization error (403)."""


class NotFoundError(SigfoxCLIError):
    """Resource not found error (404)."""


class APIError(SigfoxCLIError):
    """Sigfox API error."""

    def __init__(self, message: str, status_code: int | None = None, response_body: str | None = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body


class NetworkError(SigfoxCLIError):
    """Network connection error."""


class ValidationError(SigfoxCLIError):
    """Input validation error."""
