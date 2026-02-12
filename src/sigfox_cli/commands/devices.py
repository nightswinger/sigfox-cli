"""Device commands."""

from typing import Any

import click
from sigfox.models import DeviceCreate, DeviceUpdate

from . import get_sigfox_from_config
from ..config import load_config
from ..exceptions import ConfigError, SigfoxCLIError
from ..output import (
    output_device_detail,
    output_device_list,
    output_message_list,
    print_error,
    print_info,
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
        client = get_sigfox_from_config(api_login, api_password)
        cfg = load_config()
        output_format = output or cfg.output_format

        # Convert comma-separated group IDs to list
        group_ids_list = group_ids.split(",") if group_ids else None

        # Fetch devices using high-level API
        with client:
            devices = client.devices.list(
                limit=limit,
                offset=offset,
                device_type_id=device_type_id,
                group_ids=group_ids_list,
                deep=deep,
                sort=sort,
            )

            if not devices:
                print_info("No devices found.")
                return

            # Convert Pydantic models to dicts for output
            devices_data = [d.model_dump(by_alias=True) for d in devices]
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
        client = get_sigfox_from_config(api_login, api_password)
        cfg = load_config()
        output_format = output or cfg.output_format

        # Fetch device using high-level API
        with client:
            device = client.devices.get(device_id)
            device_data = device.model_dump(by_alias=True)
            output_device_detail(device_data, output_format)

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
        client = get_sigfox_from_config(api_login, api_password)
        cfg = load_config()
        output_format = output or cfg.output_format

        # Fetch messages using high-level API
        with client:
            messages = client.devices.messages(
                device_id=device_id,
                limit=limit,
                offset=offset,
                since=since,
                before=before,
            )

            if not messages:
                print_info("No messages found.")
                return

            # Convert Pydantic models to dicts for output
            messages_data = [m.model_dump(by_alias=True) for m in messages]
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
        client = get_sigfox_from_config(api_login, api_password)
        cfg = load_config()
        output_format = output or cfg.output_format

        # Build product certificate if provided
        product_cert = {"key": product_certificate} if product_certificate else None

        # Create DeviceCreate model
        device_data = DeviceCreate(
            id=device_id,
            name=name,
            device_type_id=device_type_id,
            pac=pac,
            lat=lat,
            lng=lng,
            product_certificate=product_cert,
            prototype=prototype,
            automatic_renewal=automatic_renewal,
            activable=activable,
        )

        # Create device using high-level API
        with client:
            created_device = client.devices.create(device_data)
            print_info(f"Device created successfully: {created_device.id}")

            # Display the created device
            device_dict = created_device.model_dump(by_alias=True)
            output_device_detail(device_dict, output_format)

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
        client = get_sigfox_from_config(api_login, api_password)

        # Check if any fields are specified
        has_updates = any([
            name is not None,
            lat is not None,
            lng is not None,
            product_certificate is not None,
            prototype is not None,
            automatic_renewal is not None,
            activable is not None,
        ])

        if not has_updates:
            print_error("No update fields specified. Use --name, --lat, --lng, etc.")
            raise click.Abort()

        # Build product certificate if provided
        product_cert = {"key": product_certificate} if product_certificate is not None else None

        # Create DeviceUpdate model
        device_update = DeviceUpdate(
            name=name,
            lat=lat,
            lng=lng,
            product_certificate=product_cert,
            prototype=prototype,
            automatic_renewal=automatic_renewal,
            activable=activable,
        )

        # Update device using high-level API
        with client:
            client.devices.update(device_id, device_update)
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

        client = get_sigfox_from_config(api_login, api_password)

        # Delete device using high-level API
        with client:
            client.devices.delete(device_id)
            print_info(f"Device {device_id} deleted successfully.")

    except click.Abort:
        raise
    except SigfoxCLIError as e:
        print_error(str(e))
        raise click.Abort()
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise click.Abort()
