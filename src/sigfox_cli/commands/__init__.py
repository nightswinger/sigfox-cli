"""Shared utilities for CLI commands."""

from sigfox import Sigfox, SigfoxClient

from ..config import load_config
from ..exceptions import ConfigError


def get_client_from_config(api_login: str | None, api_password: str | None) -> SigfoxClient:
    """Get Sigfox API client from configuration or CLI args.

    Args:
        api_login: Optional API login from CLI
        api_password: Optional API password from CLI

    Returns:
        Configured SigfoxClient

    Raises:
        ConfigError: If credentials are not configured
    """
    cfg = load_config()

    # Use CLI args if provided, otherwise use config
    login = api_login or cfg.api_login
    password = api_password or cfg.get_password()

    if not login or not password:
        raise ConfigError(
            "API credentials not configured. "
            "Run 'sigfox config init' or provide --api-login and --api-password options."
        )

    return SigfoxClient(
        api_login=login,
        api_password=password,
        base_url=cfg.api_base_url,
        timeout=cfg.timeout,
    )


def get_sigfox_from_config(api_login: str | None, api_password: str | None) -> Sigfox:
    """Get high-level Sigfox API client from configuration or CLI args.

    Args:
        api_login: Optional API login from CLI
        api_password: Optional API password from CLI

    Returns:
        Configured Sigfox client with high-level API access

    Raises:
        ConfigError: If credentials are not configured
    """
    cfg = load_config()

    # Use CLI args if provided, otherwise use config
    login = api_login or cfg.api_login
    password = api_password or cfg.get_password()

    if not login or not password:
        raise ConfigError(
            "API credentials not configured. "
            "Run 'sigfox config init' or provide --api-login and --api-password options."
        )

    return Sigfox(
        login=login,
        password=password,
        base_url=cfg.api_base_url,
        timeout=cfg.timeout,
    )


__all__ = ["get_client_from_config", "get_sigfox_from_config"]
