"""Configuration management for Sigfox CLI."""

from pathlib import Path
from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class SigfoxConfig(BaseSettings):
    """Sigfox CLI configuration.

    Configuration is loaded from (in order of priority):
    1. Environment variables (SIGFOX_API_LOGIN, SIGFOX_API_PASSWORD)
    2. .env file in current directory
    3. Config file at ~/.config/sigfox-cli/config.toml
    """

    model_config = SettingsConfigDict(
        env_prefix="SIGFOX_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    api_login: str | None = Field(
        default=None,
        description="Sigfox API login (ID)",
    )
    api_password: SecretStr | None = Field(
        default=None,
        description="Sigfox API password (secret)",
    )
    api_base_url: str = Field(
        default="https://api.sigfox.com/v2",
        description="Sigfox API base URL",
    )
    output_format: Literal["table", "json"] = Field(
        default="table",
        description="Default output format",
    )
    timeout: int = Field(
        default=30,
        description="HTTP request timeout in seconds",
        ge=1,
        le=300,
    )

    @property
    def is_configured(self) -> bool:
        """Check if API credentials are configured."""
        return self.api_login is not None and self.api_password is not None

    def get_password(self) -> str | None:
        """Get the password as a string."""
        if self.api_password is None:
            return None
        return self.api_password.get_secret_value()


def get_config_dir() -> Path:
    """Get the configuration directory path."""
    config_dir = Path.home() / ".config" / "sigfox-cli"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def get_config_file() -> Path:
    """Get the configuration file path."""
    return get_config_dir() / "config.toml"


def load_config() -> SigfoxConfig:
    """Load configuration from environment and config file."""
    config = SigfoxConfig()

    # Try to load from TOML config file
    config_file = get_config_file()
    if config_file.exists():
        import tomllib

        with open(config_file, "rb") as f:
            toml_data = tomllib.load(f)
            auth = toml_data.get("auth", {})
            api = toml_data.get("api", {})
            output = toml_data.get("output", {})

            # Override with TOML values if not set by env
            if config.api_login is None and "api_login" in auth:
                config.api_login = auth["api_login"]
            if config.api_password is None and "api_password" in auth:
                config.api_password = SecretStr(auth["api_password"])
            if "base_url" in api:
                config.api_base_url = api["base_url"]
            if "default_format" in output:
                config.output_format = output["default_format"]
            if "timeout" in api:
                config.timeout = api["timeout"]

    return config


def save_config(
    api_login: str | None = None,
    api_password: str | None = None,
    api_base_url: str | None = None,
    output_format: str | None = None,
    timeout: int | None = None,
) -> None:
    """Save configuration to TOML file."""
    config_file = get_config_file()

    # Load existing config if it exists
    import tomllib

    config_data = {}
    if config_file.exists():
        with open(config_file, "rb") as f:
            config_data = tomllib.load(f)

    # Update with new values
    if api_login is not None or api_password is not None:
        if "auth" not in config_data:
            config_data["auth"] = {}
        if api_login is not None:
            config_data["auth"]["api_login"] = api_login
        if api_password is not None:
            config_data["auth"]["api_password"] = api_password

    if api_base_url is not None or timeout is not None:
        if "api" not in config_data:
            config_data["api"] = {}
        if api_base_url is not None:
            config_data["api"]["base_url"] = api_base_url
        if timeout is not None:
            config_data["api"]["timeout"] = timeout

    if output_format is not None:
        if "output" not in config_data:
            config_data["output"] = {}
        config_data["output"]["default_format"] = output_format

    # Write to file
    import tomli_w

    with open(config_file, "wb") as f:
        tomli_w.dump(config_data, f)

    # Set proper permissions (read/write for owner only)
    config_file.chmod(0o600)
