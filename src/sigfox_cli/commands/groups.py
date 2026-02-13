"""Group commands."""

from typing import Any

import click
from sigfox.models import GroupCreate, GroupUpdate

from . import get_sigfox_from_config
from ..config import load_config
from ..exceptions import ConfigError, SigfoxCLIError
from ..output import (
    output_callback_error_list,
    output_geoloc_payload_list,
    output_group_detail,
    output_group_list,
    print_error,
    print_info,
    print_success,
)


@click.group(name="groups")
def groups():
    """Manage Sigfox groups."""
    pass


@groups.command(name="list")
@click.option("--limit", type=int, default=100, help="Maximum number of groups to fetch")
@click.option("--offset", type=int, default=0, help="Number of groups to skip")
@click.option("--parent-ids", help="Filter by parent group IDs (comma-separated)")
@click.option("--deep", is_flag=True, default=False, help="Retrieve all sub-groups recursively")
@click.option("--name", help="Filter by group name (contains match)")
@click.option("--types", help="Filter by group types (comma-separated integers, e.g., '0,2,8')")
@click.option("--fields", help="Additional fields to return (e.g., 'path(name,type,level)')")
@click.option(
    "--action",
    type=click.Choice([
        "base-stations:create",
        "contract-infos:create",
        "device-types:create",
        "devices:create",
        "hosts:create",
        "maintenances:create",
        "providers:create",
        "sites:create",
        "users:create",
    ]),
    help="Filter by resource:action pair",
)
@click.option(
    "--sort",
    type=click.Choice(["id", "-id", "name", "-name"]),
    help="Sort field",
)
@click.option("--authorizations", is_flag=True, default=False, help="Return user's actions and resources")
@click.option("--page-id", help="Pagination token for the page to retrieve")
@click.option(
    "--output", "-o",
    type=click.Choice(["table", "json"]),
    help="Output format",
)
@click.option("--api-login", envvar="SIGFOX_API_LOGIN", help="API login (ID)")
@click.option("--api-password", envvar="SIGFOX_API_PASSWORD", help="API password (secret)")
def list_groups(
    limit: int,
    offset: int,
    parent_ids: str | None,
    deep: bool,
    name: str | None,
    types: str | None,
    fields: str | None,
    action: str | None,
    sort: str | None,
    authorizations: bool,
    page_id: str | None,
    output: str | None,
    api_login: str | None,
    api_password: str | None,
):
    """List groups.

    Examples:
        sigfox groups list
        sigfox groups list --limit 50
        sigfox groups list --parent-ids abc123,def456 --deep
        sigfox groups list --name "My Group"
        sigfox groups list --types 0,2,8
        sigfox groups list --sort name
        sigfox groups list --output json
    """
    try:
        client = get_sigfox_from_config(api_login, api_password)
        cfg = load_config()
        output_format = output or cfg.output_format

        parent_ids_list = parent_ids.split(",") if parent_ids else None
        types_list = [int(t.strip()) for t in types.split(",")] if types else None

        with client:
            result = client.groups.list(
                limit=limit,
                offset=offset,
                parent_ids=parent_ids_list,
                deep=deep,
                name=name,
                types=types_list,
                fields=fields,
                action=action,
                sort=sort,
                authorizations=authorizations,
                page_id=page_id,
            )

            if not result:
                print_info("No groups found.")
                return

            data = [g.model_dump(by_alias=True) for g in result]
            output_group_list(data, output_format)

    except SigfoxCLIError as e:
        print_error(str(e))
        raise click.Abort()
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise click.Abort()


@groups.command(name="get")
@click.argument("group_id")
@click.option("--fields", help="Additional fields to return (e.g., 'paths(name)')")
@click.option("--authorizations", is_flag=True, default=False, help="Return user's actions and resources")
@click.option(
    "--output", "-o",
    type=click.Choice(["table", "json"]),
    help="Output format",
)
@click.option("--api-login", envvar="SIGFOX_API_LOGIN", help="API login (ID)")
@click.option("--api-password", envvar="SIGFOX_API_PASSWORD", help="API password (secret)")
def get_group(
    group_id: str,
    fields: str | None,
    authorizations: bool,
    output: str | None,
    api_login: str | None,
    api_password: str | None,
):
    """Get group details.

    Examples:
        sigfox groups get 572f1204017975032d8ec1dd
        sigfox groups get 572f1204017975032d8ec1dd --authorizations
        sigfox groups get 572f1204017975032d8ec1dd --output json
    """
    try:
        client = get_sigfox_from_config(api_login, api_password)
        cfg = load_config()
        output_format = output or cfg.output_format

        with client:
            group = client.groups.get(group_id, fields=fields, authorizations=authorizations)
            group_data = group.model_dump(by_alias=True)
            output_group_detail(group_data, output_format)

    except SigfoxCLIError as e:
        print_error(str(e))
        raise click.Abort()
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise click.Abort()


@groups.command(name="create")
@click.option("--name", required=True, help="Group name (3-100 characters)")
@click.option("--description", required=True, help="Group description (max 300 characters)")
@click.option("--type", "group_type", required=True, type=int, help="Group type (0=SO, 2=Other, 5=SVNO, 6=Partners, 7=NIP, 8=DIST, 9=Channel, 10=Starter, 11=Partner)")
@click.option("--timezone", required=True, help="Timezone (Java TimeZone ID, e.g., 'Europe/Paris')")
@click.option("--parent-id", required=True, help="Parent group ID")
@click.option("--technical-email", help="Technical contact email")
@click.option("--account-id", help="Account ID to link to the group")
@click.option("--network-operator-id", help="Network operator group ID (required for DIST & SVNO)")
@click.option("--country-iso", help="Country ISO code (3 letters, for SO and NIP)")
@click.option("--billable", type=bool, help="Whether the group is billable")
@click.option("--max-prototypes", type=int, help="Max prototypes allowed")
@click.option(
    "--output", "-o",
    type=click.Choice(["table", "json"]),
    help="Output format",
)
@click.option("--api-login", envvar="SIGFOX_API_LOGIN", help="API login (ID)")
@click.option("--api-password", envvar="SIGFOX_API_PASSWORD", help="API password (secret)")
def create_group(
    name: str,
    description: str,
    group_type: int,
    timezone: str,
    parent_id: str,
    technical_email: str | None,
    account_id: str | None,
    network_operator_id: str | None,
    country_iso: str | None,
    billable: bool | None,
    max_prototypes: int | None,
    output: str | None,
    api_login: str | None,
    api_password: str | None,
):
    """Create a new group.

    Examples:
        sigfox groups create --name "My Group" --description "Test group" --type 8 --timezone "Europe/Paris" --parent-id abc123
        sigfox groups create --name "SVNO Group" --description "SVNO" --type 5 --timezone "Europe/Paris" --parent-id abc123 --network-operator-id def456
    """
    try:
        client = get_sigfox_from_config(api_login, api_password)
        cfg = load_config()
        output_format = output or cfg.output_format

        group_data = GroupCreate(
            name=name,
            description=description,
            type=group_type,
            timezone=timezone,
            parent_id=parent_id,
            technical_email=technical_email,
            account_id=account_id,
            network_operator_id=network_operator_id,
            country_iso_alpha3=country_iso,
            billable=billable,
            max_prototype_allowed=max_prototypes,
        )

        with client:
            result = client.groups.create(group_data)
            group_id = result.get("id", "unknown")
            print_success(f"Group created successfully (ID: {group_id})")

            # Fetch and display the created group
            group = client.groups.get(group_id)
            output_group_detail(group.model_dump(by_alias=True), output_format)

    except SigfoxCLIError as e:
        print_error(str(e))
        raise click.Abort()
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise click.Abort()


@groups.command(name="update")
@click.argument("group_id")
@click.option("--name", help="Group name (3-100 characters)")
@click.option("--description", help="Group description (max 300 characters)")
@click.option("--type", "group_type", type=int, help="Group type")
@click.option("--timezone", help="Timezone (Java TimeZone ID)")
@click.option("--billable", type=bool, help="Whether the group is billable")
@click.option("--technical-email", help="Technical contact email")
@click.option("--max-prototypes", type=int, help="Max prototypes allowed")
@click.option("--api-login", envvar="SIGFOX_API_LOGIN", help="API login (ID)")
@click.option("--api-password", envvar="SIGFOX_API_PASSWORD", help="API password (secret)")
def update_group(
    group_id: str,
    name: str | None,
    description: str | None,
    group_type: int | None,
    timezone: str | None,
    billable: bool | None,
    technical_email: str | None,
    max_prototypes: int | None,
    api_login: str | None,
    api_password: str | None,
):
    """Update a group.

    Examples:
        sigfox groups update 572f1204017975032d8ec1dd --name "New Name"
        sigfox groups update 572f1204017975032d8ec1dd --description "Updated desc" --timezone "America/New_York"
    """
    try:
        client = get_sigfox_from_config(api_login, api_password)

        has_updates = any([
            name is not None,
            description is not None,
            group_type is not None,
            timezone is not None,
            billable is not None,
            technical_email is not None,
            max_prototypes is not None,
        ])

        if not has_updates:
            print_error("No update fields specified. Use --name, --description, --timezone, etc.")
            raise click.Abort()

        group_update = GroupUpdate(
            name=name,
            description=description,
            type=group_type,
            timezone=timezone,
            billable=billable,
            technical_email=technical_email,
            max_prototype_allowed=max_prototypes,
        )

        with client:
            client.groups.update(group_id, group_update)
            print_success(f"Group {group_id} updated successfully.")

    except SigfoxCLIError as e:
        print_error(str(e))
        raise click.Abort()
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise click.Abort()


@groups.command(name="delete")
@click.argument("group_id")
@click.option("--force", "-f", is_flag=True, default=False, help="Skip confirmation prompt")
@click.option("--api-login", envvar="SIGFOX_API_LOGIN", help="API login (ID)")
@click.option("--api-password", envvar="SIGFOX_API_PASSWORD", help="API password (secret)")
def delete_group(
    group_id: str,
    force: bool,
    api_login: str | None,
    api_password: str | None,
):
    """Delete a group.

    Examples:
        sigfox groups delete 572f1204017975032d8ec1dd
        sigfox groups delete 572f1204017975032d8ec1dd --force
    """
    try:
        if not force:
            click.confirm(
                f"Are you sure you want to delete group {group_id}?",
                abort=True,
            )

        client = get_sigfox_from_config(api_login, api_password)

        with client:
            client.groups.delete(group_id)
            print_success(f"Group {group_id} deleted successfully.")

    except click.Abort:
        raise
    except SigfoxCLIError as e:
        print_error(str(e))
        raise click.Abort()
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise click.Abort()


@groups.command(name="callbacks-not-delivered")
@click.argument("group_id")
@click.option("--since", type=int, help="Starting timestamp (milliseconds since Unix epoch)")
@click.option("--before", type=int, help="Ending timestamp (milliseconds since Unix epoch)")
@click.option("--limit", type=int, default=100, help="Maximum number of items to fetch")
@click.option("--offset", type=int, default=0, help="Number of items to skip")
@click.option(
    "--output", "-o",
    type=click.Choice(["table", "json"]),
    help="Output format",
)
@click.option("--api-login", envvar="SIGFOX_API_LOGIN", help="API login (ID)")
@click.option("--api-password", envvar="SIGFOX_API_PASSWORD", help="API password (secret)")
def callbacks_not_delivered(
    group_id: str,
    since: int | None,
    before: int | None,
    limit: int,
    offset: int,
    output: str | None,
    api_login: str | None,
    api_password: str | None,
):
    """List undelivered callbacks for a group.

    Examples:
        sigfox groups callbacks-not-delivered abc123
        sigfox groups callbacks-not-delivered abc123 --since 1609459200000
        sigfox groups callbacks-not-delivered abc123 --limit 50
        sigfox groups callbacks-not-delivered abc123 --output json
    """
    try:
        client = get_sigfox_from_config(api_login, api_password)
        cfg = load_config()
        output_format = output or cfg.output_format

        with client:
            errors = client.groups.callbacks_not_delivered(
                group_id=group_id,
                since=since,
                before=before,
                limit=limit,
                offset=offset,
            )

            if not errors:
                print_info("No undelivered callbacks found.")
                return

            data = [e.model_dump(by_alias=True) for e in errors]
            output_callback_error_list(data, output_format)

    except SigfoxCLIError as e:
        print_error(str(e))
        raise click.Abort()
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise click.Abort()


@groups.command(name="geoloc-payloads")
@click.argument("group_id")
@click.option("--limit", type=int, default=100, help="Maximum number of items to fetch")
@click.option("--offset", type=int, default=0, help="Number of items to skip")
@click.option("--page-id", help="Pagination token for the page to retrieve")
@click.option(
    "--output", "-o",
    type=click.Choice(["table", "json"]),
    help="Output format",
)
@click.option("--api-login", envvar="SIGFOX_API_LOGIN", help="API login (ID)")
@click.option("--api-password", envvar="SIGFOX_API_PASSWORD", help="API password (secret)")
def geoloc_payloads(
    group_id: str,
    limit: int,
    offset: int,
    page_id: str | None,
    output: str | None,
    api_login: str | None,
    api_password: str | None,
):
    """List geolocation payloads for a group.

    Examples:
        sigfox groups geoloc-payloads abc123
        sigfox groups geoloc-payloads abc123 --limit 50
        sigfox groups geoloc-payloads abc123 --output json
    """
    try:
        client = get_sigfox_from_config(api_login, api_password)
        cfg = load_config()
        output_format = output or cfg.output_format

        with client:
            payloads = client.groups.geoloc_payloads(
                group_id=group_id,
                limit=limit,
                offset=offset,
                page_id=page_id,
            )

            if not payloads:
                print_info("No geolocation payloads found.")
                return

            data = [p.model_dump(by_alias=True) for p in payloads]
            output_geoloc_payload_list(data, output_format)

    except SigfoxCLIError as e:
        print_error(str(e))
        raise click.Abort()
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise click.Abort()
