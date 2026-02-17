"""API user commands."""

import click
from sigfox.models import ApiUserCreate, ApiUserUpdate

from . import get_sigfox_from_config
from ..config import load_config
from ..exceptions import SigfoxCLIError
from ..output import (
    output_api_user_detail,
    output_api_user_list,
    output_json,
    print_error,
    print_info,
    print_success,
    print_warning,
)


@click.group(name="api-users")
def api_users():
    """Manage Sigfox API users."""
    pass


@api_users.command(name="list")
@click.option(
    "--limit", type=int, default=100, help="Maximum number of API users to fetch"
)
@click.option("--offset", type=int, default=0, help="Number of API users to skip")
@click.option("--profile-id", help="Filter by profile ID")
@click.option("--group-ids", help="Filter by group IDs (comma-separated)")
@click.option(
    "--fields",
    type=click.Choice([
        "group(name,type,level,bssId,customerBssId)",
        "profiles(name,roles(name,perms(name)))",
    ]),
    help="Additional fields to return",
)
@click.option(
    "--authorizations",
    is_flag=True,
    default=False,
    help="Return user's actions and resources",
)
@click.option(
    "--output",
    "-o",
    type=click.Choice(["table", "json"]),
    help="Output format",
)
@click.option("--api-login", envvar="SIGFOX_API_LOGIN", help="API login (ID)")
@click.option(
    "--api-password", envvar="SIGFOX_API_PASSWORD", help="API password (secret)"
)
def list_api_users(
    limit: int,
    offset: int,
    profile_id: str | None,
    group_ids: str | None,
    fields: str | None,
    authorizations: bool,
    output: str | None,
    api_login: str | None,
    api_password: str | None,
):
    """List API users.

    Examples:
        sigfox api-users list
        sigfox api-users list --limit 50
        sigfox api-users list --profile-id 5138e7dfa2f1fffaf25fd409
        sigfox api-users list --group-ids abc123,def456
        sigfox api-users list --output json
    """
    try:
        client = get_sigfox_from_config(api_login, api_password)
        cfg = load_config()
        output_format = output or cfg.output_format

        group_ids_list = group_ids.split(",") if group_ids else None

        with client:
            result = client.api_users.list(
                limit=limit,
                offset=offset,
                profile_id=profile_id,
                group_ids=group_ids_list,
                fields=fields,
                authorizations=authorizations,
            )

            if not result:
                print_info("No API users found.")
                return

            data = [u.model_dump(by_alias=True) for u in result]
            output_api_user_list(data, output_format)

    except SigfoxCLIError as e:
        print_error(str(e))
        raise click.Abort()
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise click.Abort()


@api_users.command(name="get")
@click.argument("api_user_id")
@click.option(
    "--fields",
    type=click.Choice([
        "group(name,type,level,bssId,customerBssId)",
        "profiles(name,roles(name,perms(name)))",
    ]),
    help="Additional fields to return",
)
@click.option(
    "--authorizations",
    is_flag=True,
    default=False,
    help="Return user's actions and resources",
)
@click.option(
    "--output",
    "-o",
    type=click.Choice(["table", "json"]),
    help="Output format",
)
@click.option("--api-login", envvar="SIGFOX_API_LOGIN", help="API login (ID)")
@click.option(
    "--api-password", envvar="SIGFOX_API_PASSWORD", help="API password (secret)"
)
def get_api_user(
    api_user_id: str,
    fields: str | None,
    authorizations: bool,
    output: str | None,
    api_login: str | None,
    api_password: str | None,
):
    """Get API user details.

    Examples:
        sigfox api-users get 5138e7dfa2f1fffaf25fd409
        sigfox api-users get 5138e7dfa2f1fffaf25fd409 --authorizations
        sigfox api-users get 5138e7dfa2f1fffaf25fd409 --output json
    """
    try:
        client = get_sigfox_from_config(api_login, api_password)
        cfg = load_config()
        output_format = output or cfg.output_format

        with client:
            user = client.api_users.get(
                api_user_id, fields=fields, authorizations=authorizations
            )
            user_data = user.model_dump(by_alias=True)
            output_api_user_detail(user_data, output_format)

    except SigfoxCLIError as e:
        print_error(str(e))
        raise click.Abort()
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise click.Abort()


@api_users.command(name="create")
@click.option("--group-id", required=True, help="Group ID to associate the API user to")
@click.option("--name", required=True, help="API user name (max 100 characters)")
@click.option(
    "--timezone",
    required=True,
    help="Timezone (Java TimeZone ID, e.g., 'Europe/Paris')",
)
@click.option("--profile-ids", required=True, help="Profile IDs (comma-separated)")
@click.option(
    "--output",
    "-o",
    type=click.Choice(["table", "json"]),
    help="Output format",
)
@click.option("--api-login", envvar="SIGFOX_API_LOGIN", help="API login (ID)")
@click.option(
    "--api-password", envvar="SIGFOX_API_PASSWORD", help="API password (secret)"
)
def create_api_user(
    group_id: str,
    name: str,
    timezone: str,
    profile_ids: str,
    output: str | None,
    api_login: str | None,
    api_password: str | None,
):
    """Create a new API user.

    Examples:
        sigfox api-users create --group-id abc123 --name "My API User" \\
            --timezone "Europe/Paris" --profile-ids prof1,prof2
    """
    try:
        client = get_sigfox_from_config(api_login, api_password)
        cfg = load_config()
        output_format = output or cfg.output_format

        profile_ids_list = [p.strip() for p in profile_ids.split(",")]

        user_data = ApiUserCreate(
            group_id=group_id,
            name=name,
            timezone=timezone,
            profile_ids=profile_ids_list,
        )

        with client:
            result = client.api_users.create(user_data)
            user_id = result.get("id", "unknown")
            print_success(f"API user created successfully (ID: {user_id})")

            # Fetch and display the created API user
            user = client.api_users.get(user_id)
            output_api_user_detail(user.model_dump(by_alias=True), output_format)

    except SigfoxCLIError as e:
        print_error(str(e))
        raise click.Abort()
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise click.Abort()


@api_users.command(name="update")
@click.argument("api_user_id")
@click.option("--name", help="API user name (max 100 characters)")
@click.option("--timezone", help="Timezone (Java TimeZone ID)")
@click.option("--profile-ids", help="Profile IDs (comma-separated, replaces existing)")
@click.option("--api-login", envvar="SIGFOX_API_LOGIN", help="API login (ID)")
@click.option(
    "--api-password", envvar="SIGFOX_API_PASSWORD", help="API password (secret)"
)
def update_api_user(
    api_user_id: str,
    name: str | None,
    timezone: str | None,
    profile_ids: str | None,
    api_login: str | None,
    api_password: str | None,
):
    """Update an API user.

    Examples:
        sigfox api-users update 5138e7dfa2f1fffaf25fd409 --name "New Name"
        sigfox api-users update 5138e7dfa2f1fffaf25fd409 --timezone "America/New_York"
        sigfox api-users update 5138e7dfa2f1fffaf25fd409 --profile-ids prof1,prof2
    """
    try:
        client = get_sigfox_from_config(api_login, api_password)

        has_updates = any([
            name is not None,
            timezone is not None,
            profile_ids is not None,
        ])

        if not has_updates:
            print_error(
                "No update fields specified. Use --name, --timezone, --profile-ids."
            )
            raise click.Abort()

        profile_ids_list = (
            [p.strip() for p in profile_ids.split(",")]
            if profile_ids is not None
            else None
        )

        user_update = ApiUserUpdate(
            name=name,
            timezone=timezone,
            profile_ids=profile_ids_list,
        )

        with client:
            client.api_users.update(api_user_id, user_update)
            print_success(f"API user {api_user_id} updated successfully.")

    except SigfoxCLIError as e:
        print_error(str(e))
        raise click.Abort()
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise click.Abort()


@api_users.command(name="delete")
@click.argument("api_user_id")
@click.option(
    "--force", "-f", is_flag=True, default=False, help="Skip confirmation prompt"
)
@click.option("--api-login", envvar="SIGFOX_API_LOGIN", help="API login (ID)")
@click.option(
    "--api-password", envvar="SIGFOX_API_PASSWORD", help="API password (secret)"
)
def delete_api_user(
    api_user_id: str,
    force: bool,
    api_login: str | None,
    api_password: str | None,
):
    """Delete an API user.

    Examples:
        sigfox api-users delete 5138e7dfa2f1fffaf25fd409
        sigfox api-users delete 5138e7dfa2f1fffaf25fd409 --force
    """
    try:
        if not force:
            click.confirm(
                f"Are you sure you want to delete API user {api_user_id}?",
                abort=True,
            )

        client = get_sigfox_from_config(api_login, api_password)

        with client:
            client.api_users.delete(api_user_id)
            print_success(f"API user {api_user_id} deleted successfully.")

    except click.Abort:
        raise
    except SigfoxCLIError as e:
        print_error(str(e))
        raise click.Abort()
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise click.Abort()


@api_users.command(name="add-profiles")
@click.argument("api_user_id")
@click.option(
    "--profile-ids", required=True, help="Profile IDs to associate (comma-separated)"
)
@click.option("--api-login", envvar="SIGFOX_API_LOGIN", help="API login (ID)")
@click.option(
    "--api-password", envvar="SIGFOX_API_PASSWORD", help="API password (secret)"
)
def add_profiles(
    api_user_id: str,
    profile_ids: str,
    api_login: str | None,
    api_password: str | None,
):
    """Associate profiles to an API user.

    Examples:
        sigfox api-users add-profiles 5138e7dfa2f1fffaf25fd409 --profile-ids prof1,prof2
    """
    try:
        client = get_sigfox_from_config(api_login, api_password)
        profile_ids_list = [p.strip() for p in profile_ids.split(",")]

        with client:
            client.api_users.add_profiles(api_user_id, profile_ids_list)
            print_success(
                f"Profiles associated to API user {api_user_id} successfully."
            )

    except SigfoxCLIError as e:
        print_error(str(e))
        raise click.Abort()
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise click.Abort()


@api_users.command(name="remove-profile")
@click.argument("api_user_id")
@click.argument("profile_id")
@click.option(
    "--force", "-f", is_flag=True, default=False, help="Skip confirmation prompt"
)
@click.option("--api-login", envvar="SIGFOX_API_LOGIN", help="API login (ID)")
@click.option(
    "--api-password", envvar="SIGFOX_API_PASSWORD", help="API password (secret)"
)
def remove_profile(
    api_user_id: str,
    profile_id: str,
    force: bool,
    api_login: str | None,
    api_password: str | None,
):
    """Remove a profile from an API user.

    Examples:
        sigfox api-users remove-profile 5138e7dfa2f1fffaf25fd409 51cc7155e4b00d18ddb99230
        sigfox api-users remove-profile 5138e7dfa2f1fffaf25fd409 51cc7155e4b00d18ddb99230 --force
    """
    try:
        if not force:
            click.confirm(
                f"Are you sure you want to remove profile {profile_id} from API user {api_user_id}?",
                abort=True,
            )

        client = get_sigfox_from_config(api_login, api_password)

        with client:
            client.api_users.remove_profile(api_user_id, profile_id)
            print_success(
                f"Profile {profile_id} removed from API user {api_user_id} successfully."
            )

    except click.Abort:
        raise
    except SigfoxCLIError as e:
        print_error(str(e))
        raise click.Abort()
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise click.Abort()


@api_users.command(name="renew-credential")
@click.argument("api_user_id")
@click.option(
    "--force", "-f", is_flag=True, default=False, help="Skip confirmation prompt"
)
@click.option(
    "--output",
    "-o",
    type=click.Choice(["table", "json"]),
    help="Output format",
)
@click.option("--api-login", envvar="SIGFOX_API_LOGIN", help="API login (ID)")
@click.option(
    "--api-password", envvar="SIGFOX_API_PASSWORD", help="API password (secret)"
)
def renew_credential(
    api_user_id: str,
    force: bool,
    output: str | None,
    api_login: str | None,
    api_password: str | None,
):
    """Generate a new password for an API user.

    WARNING: This invalidates the current password immediately.

    Examples:
        sigfox api-users renew-credential 5138e7dfa2f1fffaf25fd409
        sigfox api-users renew-credential 5138e7dfa2f1fffaf25fd409 --force
    """
    try:
        if not force:
            click.confirm(
                f"This will invalidate the current password for API user {api_user_id}. Continue?",
                abort=True,
            )

        client = get_sigfox_from_config(api_login, api_password)
        cfg = load_config()
        output_format = output or cfg.output_format

        with client:
            result = client.api_users.renew_credential(api_user_id)

            if output_format == "json":
                output_json(result)
            else:
                access_token = result.get("accessToken", "N/A")
                print_success(f"New credential generated for API user {api_user_id}.")
                print_warning(f"New access token: {access_token}")
                print_info("Save this token now -- it cannot be retrieved later.")

    except click.Abort:
        raise
    except SigfoxCLIError as e:
        print_error(str(e))
        raise click.Abort()
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise click.Abort()
