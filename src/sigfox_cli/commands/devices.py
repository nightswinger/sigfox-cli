"""Device commands."""

from typing import Any

import click

from ..client import SigfoxClient
from ..config import load_config
from ..exceptions import ConfigError, SigfoxCLIError
from ..output import (
    output_device_detail,
    output_device_list,
    output_message_list,
    print_error,
    print_info,
)


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


@click.group(name="devices")
def devices():
    """Manage Sigfox devices."""
    pass


@devices.command(name="list")
@click.option("--limit", type=int, default=100, help="Maximum number of devices to fetch")
@click.option("--offset", type=int, default=0, help="Number of devices to skip")
@click.option("--device-type-id", help="Filter by device type ID")
@click.option("--group-ids", help="Filter by group IDs (comma-separated)")
@click.option("--deep", is_flag=True, default=False, help="Search in groups and subgroups")
@click.option("--sort", help="Sort field (e.g., 'name', '-lastCom')")
@click.option(
    "--output",
    "-o",
    type=click.Choice(["table", "json"]),
    help="Output format",
)
@click.option("--api-login", envvar="SIGFOX_API_LOGIN", help="API login (ID)")
@click.option("--api-password", envvar="SIGFOX_API_PASSWORD", help="API password (secret)")
def list_devices(
    limit: int,
    offset: int,
    device_type_id: str | None,
    group_ids: str | None,
    deep: bool,
    sort: str | None,
    output: str | None,
    api_login: str | None,
    api_password: str | None,
):
    """List devices.

    Examples:
        sigfox devices list
        sigfox devices list --limit 50
        sigfox devices list --device-type-id 5d8cdc8fea06bb6e41234567
        sigfox devices list --group-ids abc123,def456 --deep
        sigfox devices list --output json
    """
    try:
        client = get_client_from_config(api_login, api_password)
        cfg = load_config()
        output_format = output or cfg.output_format

        # Build query parameters
        params: dict[str, Any] = {
            "limit": limit,
            "offset": offset,
        }

        if device_type_id:
            params["deviceTypeId"] = device_type_id
        if group_ids:
            params["groupIds"] = group_ids
        if deep:
            params["deep"] = True
        if sort:
            params["sort"] = sort

        # Fetch devices
        with client:
            response = client.get("/devices/", params=params)
            devices_data = response.get("data", [])

            if not devices_data:
                print_info("No devices found.")
                return

            output_device_list(devices_data, output_format)

    except SigfoxCLIError as e:
        print_error(str(e))
        raise click.Abort()
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise click.Abort()


@devices.command(name="get")
@click.argument("device_id")
@click.option(
    "--output",
    "-o",
    type=click.Choice(["table", "json"]),
    help="Output format",
)
@click.option("--api-login", envvar="SIGFOX_API_LOGIN", help="API login (ID)")
@click.option("--api-password", envvar="SIGFOX_API_PASSWORD", help="API password (secret)")
def get_device(
    device_id: str,
    output: str | None,
    api_login: str | None,
    api_password: str | None,
):
    """Get device details.

    Examples:
        sigfox devices get 1A2B3C
        sigfox devices get 1A2B3C --output json
    """
    try:
        client = get_client_from_config(api_login, api_password)
        cfg = load_config()
        output_format = output or cfg.output_format

        # Fetch device
        with client:
            device = client.get(f"/devices/{device_id}")
            output_device_detail(device, output_format)

    except SigfoxCLIError as e:
        print_error(str(e))
        raise click.Abort()
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise click.Abort()


@devices.command(name="messages")
@click.argument("device_id")
@click.option("--limit", type=int, default=100, help="Maximum number of messages to fetch")
@click.option("--offset", type=int, default=0, help="Number of messages to skip")
@click.option("--since", type=int, help="Starting timestamp (milliseconds since Unix epoch)")
@click.option("--before", type=int, help="Ending timestamp (milliseconds since Unix epoch)")
@click.option(
    "--output",
    "-o",
    type=click.Choice(["table", "json"]),
    help="Output format",
)
@click.option("--api-login", envvar="SIGFOX_API_LOGIN", help="API login (ID)")
@click.option("--api-password", envvar="SIGFOX_API_PASSWORD", help="API password (secret)")
def list_messages(
    device_id: str,
    limit: int,
    offset: int,
    since: int | None,
    before: int | None,
    output: str | None,
    api_login: str | None,
    api_password: str | None,
):
    """List messages for a device.

    Examples:
        sigfox devices messages 1A2B3C
        sigfox devices messages 1A2B3C --limit 50
        sigfox devices messages 1A2B3C --since 1609459200000
        sigfox devices messages 1A2B3C --output json
    """
    try:
        client = get_client_from_config(api_login, api_password)
        cfg = load_config()
        output_format = output or cfg.output_format

        # Build query parameters
        params: dict[str, Any] = {
            "limit": limit,
            "offset": offset,
        }

        if since:
            params["since"] = since
        if before:
            params["before"] = before

        # Fetch messages
        with client:
            response = client.get(f"/devices/{device_id}/messages", params=params)
            messages_data = response.get("data", [])

            if not messages_data:
                print_info("No messages found.")
                return

            output_message_list(messages_data, output_format)

    except SigfoxCLIError as e:
        print_error(str(e))
        raise click.Abort()
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise click.Abort()
