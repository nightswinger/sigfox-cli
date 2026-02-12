"""Configuration commands."""

import click

from ..config import get_config_file, load_config, save_config
from ..output import print_error, print_info, print_success


@click.group(name="config")
def config():
    """Manage Sigfox CLI configuration."""
    pass


@config.command(name="init")
def init():
    """Initialize configuration interactively."""
    print_info("Sigfox CLI Configuration Setup")
    print_info(f"Configuration will be saved to: {get_config_file()}")
    print_info("")

    # Prompt for API credentials
    api_login = click.prompt("API Login (ID)", type=str)
    api_password = click.prompt("API Password (Secret)", type=str, hide_input=True)

    # Optional settings
    api_base_url = click.prompt(
        "API Base URL",
        type=str,
        default="https://api.sigfox.com/v2",
        show_default=True,
    )
    output_format = click.prompt(
        "Default output format",
        type=click.Choice(["table", "json"]),
        default="table",
        show_default=True,
    )
    timeout = click.prompt(
        "Request timeout (seconds)",
        type=int,
        default=30,
        show_default=True,
    )

    # Save configuration
    try:
        save_config(
            api_login=api_login,
            api_password=api_password,
            api_base_url=api_base_url,
            output_format=output_format,
            timeout=timeout,
        )
        print_success(f"Configuration saved to {get_config_file()}")
        print_info("You can now use Sigfox CLI commands.")
    except Exception as e:
        print_error(f"Failed to save configuration: {e}")
        raise click.Abort()


@config.command(name="show")
def show():
    """Show current configuration."""
    try:
        cfg = load_config()

        print_info("Current Configuration:")
        print_info("")
        print_info(f"  API Login: {cfg.api_login or '[not set]'}")
        print_info(f"  API Password: {'[set]' if cfg.api_password else '[not set]'}")
        print_info(f"  API Base URL: {cfg.api_base_url}")
        print_info(f"  Default Output Format: {cfg.output_format}")
        print_info(f"  Timeout: {cfg.timeout}s")
        print_info("")
        print_info(f"Config file: {get_config_file()}")

        if not cfg.is_configured:
            print_error("API credentials are not configured.")
            print_info("Run 'sigfox config init' to set up credentials.")

    except Exception as e:
        print_error(f"Failed to load configuration: {e}")
        raise click.Abort()


@config.command(name="set")
@click.argument("key")
@click.argument("value")
def set_value(key: str, value: str):
    """Set a configuration value.

    Examples:
        sigfox config set api_login YOUR_LOGIN
        sigfox config set output_format json
    """
    valid_keys = ["api_login", "api_password", "api_base_url", "output_format", "timeout"]

    if key not in valid_keys:
        print_error(f"Invalid configuration key: {key}")
        print_info(f"Valid keys: {', '.join(valid_keys)}")
        raise click.Abort()

    try:
        # Convert value type if needed
        if key == "timeout":
            value = int(value)
        elif key == "output_format" and value not in ["table", "json"]:
            print_error(f"Invalid output format: {value}")
            print_info("Valid formats: table, json")
            raise click.Abort()

        # Save configuration
        kwargs = {key: value}
        save_config(**kwargs)

        print_success(f"Configuration updated: {key} = {value}")

    except ValueError as e:
        print_error(f"Invalid value for {key}: {e}")
        raise click.Abort()
    except Exception as e:
        print_error(f"Failed to update configuration: {e}")
        raise click.Abort()
