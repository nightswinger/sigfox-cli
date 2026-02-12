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


@devices.command(name="create")
@click.option("--device-id", required=True, help="Device ID (hexadecimal format)")
@click.option("--name", required=True, help="Device name (max 100 characters)")
@click.option("--device-type-id", required=True, help="Device type ID")
@click.option("--pac", required=True, envvar="SIGFOX_DEVICE_PAC", help="PAC (Porting Access Code)")
@click.option("--lat", type=float, help="Latitude")
@click.option("--lng", type=float, help="Longitude")
@click.option("--product-certificate", help="Product certificate key")
@click.option("--prototype", is_flag=True, default=False, help="Mark as prototype device")
@click.option("--automatic-renewal/--no-automatic-renewal", default=True, help="Enable automatic token renewal")
@click.option("--activable/--no-activable", default=True, help="Device can take a token")
@click.option(
    "--output",
    "-o",
    type=click.Choice(["table", "json"]),
    help="Output format",
)
@click.option("--api-login", envvar="SIGFOX_API_LOGIN", help="API login (ID)")
@click.option("--api-password", envvar="SIGFOX_API_PASSWORD", help="API password (secret)")
def create_device(
    device_id: str,
    name: str,
    device_type_id: str,
    pac: str,
    lat: float | None,
    lng: float | None,
    product_certificate: str | None,
    prototype: bool,
    automatic_renewal: bool,
    activable: bool,
    output: str | None,
    api_login: str | None,
    api_password: str | None,
):
    """Create a new device.

    Examples:
        sigfox devices create --device-id 1A2B3C --name "My Device" --device-type-id 5d8cdc8fea06bb6e41234567 --pac ABC123DEF456
        sigfox devices create --device-id 1A2B3C --name "Test" --device-type-id 5d8cdc8fea06bb6e41234567 --pac ABC123 --lat 48.8585715 --lng 2.2922923
        sigfox devices create --device-id 1A2B3C --name "Prototype" --device-type-id 5d8cdc8fea06bb6e41234567 --pac ABC123 --prototype
    """
    try:
        client = get_client_from_config(api_login, api_password)
        cfg = load_config()
        output_format = output or cfg.output_format

        # Build request body
        body: dict[str, Any] = {
            "id": device_id,
            "name": name,
            "deviceTypeId": device_type_id,
            "pac": pac,
            "prototype": prototype,
            "automaticRenewal": automatic_renewal,
            "activable": activable,
        }

        if lat is not None:
            body["lat"] = lat
        if lng is not None:
            body["lng"] = lng
        if product_certificate is not None:
            body["productCertificate"] = {"key": product_certificate}

        # Create device
        with client:
            result = client.post("/devices/", data=body)
            created_id = result.get("id", device_id)
            print_info(f"Device created successfully: {created_id}")

            # Fetch and display the created device
            device = client.get(f"/devices/{created_id}")
            output_device_detail(device, output_format)

    except SigfoxCLIError as e:
        print_error(str(e))
        raise click.Abort()
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise click.Abort()


@devices.command(name="update")
@click.argument("device_id")
@click.option("--name", help="Device name")
@click.option("--lat", type=float, help="Latitude")
@click.option("--lng", type=float, help="Longitude")
@click.option("--product-certificate", help="Product certificate key")
@click.option("--prototype", type=bool, help="Prototype status (true/false)")
@click.option("--automatic-renewal", type=bool, help="Automatic token renewal (true/false)")
@click.option("--activable", type=bool, help="Device can take a token (true/false)")
@click.option("--api-login", envvar="SIGFOX_API_LOGIN", help="API login (ID)")
@click.option("--api-password", envvar="SIGFOX_API_PASSWORD", help="API password (secret)")
def update_device(
    device_id: str,
    name: str | None,
    lat: float | None,
    lng: float | None,
    product_certificate: str | None,
    prototype: bool | None,
    automatic_renewal: bool | None,
    activable: bool | None,
    api_login: str | None,
    api_password: str | None,
):
    """Update a device.

    Examples:
        sigfox devices update 1A2B3C --name "New Name"
        sigfox devices update 1A2B3C --lat 48.8585715 --lng 2.2922923
        sigfox devices update 1A2B3C --prototype true
        sigfox devices update 1A2B3C --name "Updated" --automatic-renewal false
    """
    try:
        client = get_client_from_config(api_login, api_password)

        # Build request body
        body: dict[str, Any] = {}

        if name is not None:
            body["name"] = name
        if lat is not None:
            body["lat"] = lat
        if lng is not None:
            body["lng"] = lng
        if product_certificate is not None:
            body["productCertificate"] = {"key": product_certificate}
        if prototype is not None:
            body["prototype"] = prototype
        if automatic_renewal is not None:
            body["automaticRenewal"] = automatic_renewal
        if activable is not None:
            body["activable"] = activable

        if not body:
            print_error("No update fields specified. Use --name, --lat, --lng, etc.")
            raise click.Abort()

        # Update device
        with client:
            client.put(f"/devices/{device_id}", data=body)
            print_info(f"Device {device_id} updated successfully.")

    except SigfoxCLIError as e:
        print_error(str(e))
        raise click.Abort()
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise click.Abort()


@devices.command(name="delete")
@click.argument("device_id")
@click.option("--force", "-f", is_flag=True, default=False, help="Skip confirmation prompt")
@click.option("--api-login", envvar="SIGFOX_API_LOGIN", help="API login (ID)")
@click.option("--api-password", envvar="SIGFOX_API_PASSWORD", help="API password (secret)")
def delete_device(
    device_id: str,
    force: bool,
    api_login: str | None,
    api_password: str | None,
):
    """Delete a device.

    Examples:
        sigfox devices delete 1A2B3C
        sigfox devices delete 1A2B3C --force
    """
    try:
        if not force:
            click.confirm(
                f"Are you sure you want to delete device {device_id}?",
                abort=True,
            )

        client = get_client_from_config(api_login, api_password)

        # Delete device
        with client:
            client.delete(f"/devices/{device_id}")
            print_info(f"Device {device_id} deleted successfully.")

    except click.Abort:
        raise
    except SigfoxCLIError as e:
        print_error(str(e))
        raise click.Abort()
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise click.Abort()
