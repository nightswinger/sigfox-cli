"""Device type commands."""

from typing import Any

import click

from ..client import SigfoxClient
from ..config import load_config
from ..exceptions import ConfigError, SigfoxCLIError
from ..output import (
    output_device_type_detail,
    output_device_type_list,
    print_error,
    print_info,
    print_success,
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
        client = get_client_from_config(api_login, api_password)
        cfg = load_config()
        output_format = output or cfg.output_format

        # Build query parameters
        params: dict[str, Any] = {
            "limit": limit,
            "offset": offset,
        }

        if name:
            params["name"] = name
        if group_ids:
            params["groupIds"] = group_ids
        if deep:
            params["deep"] = True
        if contract_id:
            params["contractId"] = contract_id
        if sort:
            params["sort"] = sort

        # Fetch device types
        with client:
            response = client.get("/device-types/", params=params)
            data = response.get("data", [])

            if not data:
                print_info("No device types found.")
                return

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
        client = get_client_from_config(api_login, api_password)
        cfg = load_config()
        output_format = output or cfg.output_format

        # Fetch device type
        with client:
            device_type = client.get(f"/device-types/{device_type_id}")
            output_device_type_detail(device_type, output_format)

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
        client = get_client_from_config(api_login, api_password)
        cfg = load_config()
        output_format = output or cfg.output_format

        # Build request body
        body: dict[str, Any] = {
            "name": name,
            "groupId": group_id,
        }

        if description is not None:
            body["description"] = description
        if keep_alive is not None:
            body["keepAlive"] = keep_alive
        if alert_email is not None:
            body["alertEmail"] = alert_email
        if payload_type is not None:
            body["payloadType"] = payload_type
        if downlink_mode is not None:
            body["downlinkMode"] = downlink_mode
        if downlink_data is not None:
            body["downlinkDataString"] = downlink_data
        if contract_id is not None:
            body["contractId"] = contract_id

        # Create device type
        with client:
            result = client.post("/device-types/", data=body)
            print_success(f"Device type created successfully (ID: {result.get('id', 'unknown')})")
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
        client = get_client_from_config(api_login, api_password)

        # Build request body
        body: dict[str, Any] = {}

        if name is not None:
            body["name"] = name
        if description is not None:
            body["description"] = description
        if keep_alive is not None:
            body["keepAlive"] = keep_alive
        if alert_email is not None:
            body["alertEmail"] = alert_email
        if payload_type is not None:
            body["payloadType"] = payload_type
        if downlink_mode is not None:
            body["downlinkMode"] = downlink_mode
        if downlink_data is not None:
            body["downlinkDataString"] = downlink_data

        if not body:
            print_error("No update fields specified. Use --name, --description, etc.")
            raise click.Abort()

        # Update device type
        with client:
            client.put(f"/device-types/{device_type_id}", data=body)
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

        client = get_client_from_config(api_login, api_password)

        # Delete device type
        with client:
            client.delete(f"/device-types/{device_type_id}")
            print_success(f"Device type {device_type_id} deleted successfully.")

    except click.Abort:
        raise
    except SigfoxCLIError as e:
        print_error(str(e))
        raise click.Abort()
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise click.Abort()
