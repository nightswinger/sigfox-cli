"""Custom exceptions for Sigfox CLI."""

from sigfox.exceptions import (
    APIError as _APIError,
    AuthenticationError as _AuthenticationError,
    AuthorizationError as _AuthorizationError,
    NetworkError as _NetworkError,
    NotFoundError as _NotFoundError,
    SigfoxError,
    ValidationError as _ValidationError,
)


class SigfoxCLIError(SigfoxError):
    """Base exception for Sigfox CLI."""


class ConfigError(SigfoxCLIError):
    """Configuration error."""


# Re-export API exceptions from sigfox package for backward compatibility
AuthenticationError = _AuthenticationError
AuthorizationError = _AuthorizationError
NotFoundError = _NotFoundError
APIError = _APIError
NetworkError = _NetworkError
ValidationError = _ValidationError
