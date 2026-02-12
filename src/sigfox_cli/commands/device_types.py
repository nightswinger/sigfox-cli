"""Device type commands."""

from typing import Any

import click
from sigfox.models import DeviceTypeCreate, DeviceTypeUpdate

from . import get_sigfox_from_config
from ..config import load_config
from ..exceptions import ConfigError, SigfoxCLIError
from ..output import (
    output_device_type_detail,
    output_device_type_list,
    print_error,
    print_info,
    print_success,
)


@click.group(name="device-types")
def device_types():
    """Manage Sigfox device types."""
    pass


@device_types.command(name="list")
@click.option("--limit", type=int, default=100, help="Maximum number of device types to fetch")
@click.option("--offset", type=int, default=0, help="Number of device types to skip")
@click.option("--name", help="Filter by device type name (prefix match)")
@click.option("--group-ids", help="Filter by group IDs (comma-separated)")
@click.option("--deep", is_flag=True, default=False, help="Search in groups and subgroups")
@click.option("--contract-id", help="Filter by contract ID")
@click.option("--sort", help="Sort field (e.g., 'name', '-name')")
@click.option(
    "--output",
    "-o",
    type=click.Choice(["table", "json"]),
    help="Output format",
)
@click.option("--api-login", envvar="SIGFOX_API_LOGIN", help="API login (ID)")
@click.option("--api-password", envvar="SIGFOX_API_PASSWORD", help="API password (secret)")
def list_device_types(
    limit: int,
    offset: int,
    name: str | None,
    group_ids: str | None,
    deep: bool,
    contract_id: str | None,
    sort: str | None,
    output: str | None,
    api_login: str | None,
    api_password: str | None,
):
    """List device types.

    Examples:
        sigfox device-types list
        sigfox device-types list --limit 50
        sigfox device-types list --name MyType
        sigfox device-types list --group-ids abc123,def456 --deep
        sigfox device-types list --output json
    """
    try:
        client = get_sigfox_from_config(api_login, api_password)
        cfg = load_config()
        output_format = output or cfg.output_format

        # Convert comma-separated group IDs to list
        group_ids_list = group_ids.split(",") if group_ids else None

        # Fetch device types using high-level API
        with client:
            device_types = client.device_types.list(
                limit=limit,
                offset=offset,
                name=name,
                group_ids=group_ids_list,
                deep=deep,
                sort=sort,
            )

            if not device_types:
                print_info("No device types found.")
                return

            # Convert Pydantic models to dicts for output
            data = [dt.model_dump(by_alias=True) for dt in device_types]
            output_device_type_list(data, output_format)

    except SigfoxCLIError as e:
        print_error(str(e))
        raise click.Abort()
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise click.Abort()


@device_types.command(name="get")
@click.argument("device_type_id")
@click.option(
    "--output",
    "-o",
    type=click.Choice(["table", "json"]),
    help="Output format",
)
@click.option("--api-login", envvar="SIGFOX_API_LOGIN", help="API login (ID)")
@click.option("--api-password", envvar="SIGFOX_API_PASSWORD", help="API password (secret)")
def get_device_type(
    device_type_id: str,
    output: str | None,
    api_login: str | None,
    api_password: str | None,
):
    """Get device type details.

    Examples:
        sigfox device-types get 5d8cdc8fea06bb6e41234567
        sigfox device-types get 5d8cdc8fea06bb6e41234567 --output json
    """
    try:
        client = get_sigfox_from_config(api_login, api_password)
        cfg = load_config()
        output_format = output or cfg.output_format

        # Fetch device type using high-level API
        with client:
            device_type = client.device_types.get(device_type_id)
            device_type_data = device_type.model_dump(by_alias=True)
            output_device_type_detail(device_type_data, output_format)

    except SigfoxCLIError as e:
        print_error(str(e))
        raise click.Abort()
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise click.Abort()


@device_types.command(name="create")
@click.option("--name", required=True, help="Device type name")
@click.option("--group-id", required=True, help="Group ID to associate")
@click.option("--description", help="Device type description")
@click.option("--keep-alive", type=int, help="Keep alive period in seconds (0 = default)")
@click.option("--alert-email", help="Alert email address")
@click.option("--payload-type", type=int, help="Payload type (2=Regular, 3=Custom grammar, 4=Geolocation)")
@click.option("--downlink-mode", type=int, help="Downlink mode (0=DIRECT, 1=CALLBACK, 2=NONE, 3=MANAGED)")
@click.option("--downlink-data", help="Downlink data (hex string)")
@click.option("--contract-id", help="Contract ID")
@click.option(
    "--output",
    "-o",
    type=click.Choice(["table", "json"]),
    help="Output format",
)
@click.option("--api-login", envvar="SIGFOX_API_LOGIN", help="API login (ID)")
@click.option("--api-password", envvar="SIGFOX_API_PASSWORD", help="API password (secret)")
def create_device_type(
    name: str,
    group_id: str,
    description: str | None,
    keep_alive: int | None,
    alert_email: str | None,
    payload_type: int | None,
    downlink_mode: int | None,
    downlink_data: str | None,
    contract_id: str | None,
    output: str | None,
    api_login: str | None,
    api_password: str | None,
):
    """Create a new device type.

    Examples:
        sigfox device-types create --name "My Type" --group-id abc123
        sigfox device-types create --name "My Type" --group-id abc123 --description "Test" --contract-id def456
        sigfox device-types create --name "My Type" --group-id abc123 --output json
    """
    try:
        client = get_sigfox_from_config(api_login, api_password)
        cfg = load_config()
        output_format = output or cfg.output_format

        # Create DeviceTypeCreate model
        device_type_data = DeviceTypeCreate(
            name=name,
            group_id=group_id,
            description=description,
            keep_alive=keep_alive,
            alert_email=alert_email,
            payload_type=payload_type,
            downlink_mode=downlink_mode,
            downlink_data_string=downlink_data,
            contract_id=contract_id,
        )

        # Create device type using high-level API
        with client:
            created_device_type = client.device_types.create(device_type_data)
            print_success(f"Device type created successfully (ID: {created_device_type.id})")
            result = created_device_type.model_dump(by_alias=True)
            output_device_type_detail(result, output_format)

    except SigfoxCLIError as e:
        print_error(str(e))
        raise click.Abort()
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise click.Abort()


@device_types.command(name="update")
@click.argument("device_type_id")
@click.option("--name", help="Device type name")
@click.option("--description", help="Device type description")
@click.option("--keep-alive", type=int, help="Keep alive period in seconds")
@click.option("--alert-email", help="Alert email address")
@click.option("--payload-type", type=int, help="Payload type")
@click.option("--downlink-mode", type=int, help="Downlink mode")
@click.option("--downlink-data", help="Downlink data (hex string)")
@click.option("--api-login", envvar="SIGFOX_API_LOGIN", help="API login (ID)")
@click.option("--api-password", envvar="SIGFOX_API_PASSWORD", help="API password (secret)")
def update_device_type(
    device_type_id: str,
    name: str | None,
    description: str | None,
    keep_alive: int | None,
    alert_email: str | None,
    payload_type: int | None,
    downlink_mode: int | None,
    downlink_data: str | None,
    api_login: str | None,
    api_password: str | None,
):
    """Update a device type.

    Examples:
        sigfox device-types update 5d8cdc8fea06bb6e41234567 --name "New Name"
        sigfox device-types update 5d8cdc8fea06bb6e41234567 --description "Updated description"
        sigfox device-types update 5d8cdc8fea06bb6e41234567 --keep-alive 3600
    """
    try:
        client = get_sigfox_from_config(api_login, api_password)

        # Check if any fields are specified
        has_updates = any([
            name is not None,
            description is not None,
            keep_alive is not None,
            alert_email is not None,
            payload_type is not None,
            downlink_mode is not None,
            downlink_data is not None,
        ])

        if not has_updates:
            print_error("No update fields specified. Use --name, --description, etc.")
            raise click.Abort()

        # Create DeviceTypeUpdate model
        device_type_update = DeviceTypeUpdate(
            name=name,
            description=description,
            keep_alive=keep_alive,
            alert_email=alert_email,
            payload_type=payload_type,
            downlink_mode=downlink_mode,
            downlink_data_string=downlink_data,
        )

        # Update device type using high-level API
        with client:
            client.device_types.update(device_type_id, device_type_update)
            print_success(f"Device type {device_type_id} updated successfully.")

    except SigfoxCLIError as e:
        print_error(str(e))
        raise click.Abort()
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise click.Abort()


@device_types.command(name="delete")
@click.argument("device_type_id")
@click.option("--force", "-f", is_flag=True, default=False, help="Skip confirmation prompt")
@click.option("--api-login", envvar="SIGFOX_API_LOGIN", help="API login (ID)")
@click.option("--api-password", envvar="SIGFOX_API_PASSWORD", help="API password (secret)")
def delete_device_type(
    device_type_id: str,
    force: bool,
    api_login: str | None,
    api_password: str | None,
):
    """Delete a device type.

    Examples:
        sigfox device-types delete 5d8cdc8fea06bb6e41234567
        sigfox device-types delete 5d8cdc8fea06bb6e41234567 --force
    """
    try:
        if not force:
            click.confirm(
                f"Are you sure you want to delete device type {device_type_id}?",
                abort=True,
            )

        client = get_sigfox_from_config(api_login, api_password)

        # Delete device type using high-level API
        with client:
            client.device_types.delete(device_type_id)
            print_success(f"Device type {device_type_id} deleted successfully.")

    except click.Abort:
        raise
    except SigfoxCLIError as e:
        print_error(str(e))
        raise click.Abort()
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise click.Abort()
