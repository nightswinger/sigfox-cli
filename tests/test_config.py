"""Tests for configuration management."""

import pytest
from pathlib import Path
from sigfox_cli.config import SigfoxConfig, load_config, save_config
from pydantic import SecretStr


def test_sigfox_config_creation():
    """Test SigfoxConfig model creation."""
    config = SigfoxConfig(
        api_login="test_login",
        api_password=SecretStr("test_password"),
    )
    assert config.api_login == "test_login"
    assert config.get_password() == "test_password"
    assert config.is_configured is True


def test_sigfox_config_not_configured():
    """Test SigfoxConfig when credentials are not set."""
    config = SigfoxConfig()
    assert config.is_configured is False


def test_sigfox_config_defaults():
    """Test SigfoxConfig default values."""
    config = SigfoxConfig()
    assert config.api_base_url == "https://api.sigfox.com/v2"
    assert config.output_format == "table"
    assert config.timeout == 30
