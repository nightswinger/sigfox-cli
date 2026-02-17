"""User commands."""

import click
from sigfox.models import UserCreate, UserUpdate

from . import get_sigfox_from_config
from ..config import load_config
from ..exceptions import SigfoxCLIError
from ..output import (
    output_json,
    output_user_detail,
    output_user_list,
    print_error,
    print_info,
    print_success,
)


@click.group(name="users")
def users():
    """Manage Sigfox users (portal users)."""
    pass


@users.command(name="list")
@click.option(
    "--limit", type=int, default=100, help="Maximum number of users to fetch"
)
@click.option("--offset", type=int, default=0, help="Number of users to skip")
@click.option("--group-ids", help="Filter by group IDs (comma-separated)")
@click.option(
    "--deep",
    is_flag=True,
    default=False,
    help="Include users from all child groups",
)
@click.option(
    "--fields",
    help="Additional fields to return",
)
@click.option(
    "--sort",
    help="Sort results (e.g., 'firstName:asc', 'creationTime:desc')",
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
def list_users(
    limit: int,
    offset: int,
    group_ids: str | None,
    deep: bool,
    fields: str | None,
    sort: str | None,
    authorizations: bool,
    output: str | None,
    api_login: str | None,
    api_password: str | None,
):
    """List users.

    Examples:
        sigfox users list
        sigfox users list --limit 50
        sigfox users list --group-ids abc123,def456
        sigfox users list --deep
        sigfox users list --output json
    """
    try:
        client = get_sigfox_from_config(api_login, api_password)
        cfg = load_config()
        output_format = output or cfg.output_format

        group_ids_list = group_ids.split(",") if group_ids else None

        with client:
            result = client.users.list(
                limit=limit,
                offset=offset,
                group_ids=group_ids_list,
                deep=deep,
                fields=fields,
                sort=sort,
                authorizations=authorizations,
            )

            if not result:
                print_info("No users found.")
                return

            data = [u.model_dump(by_alias=True) for u in result]
            output_user_list(data, output_format)

    except SigfoxCLIError as e:
        print_error(str(e))
        raise click.Abort()
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise click.Abort()


@users.command(name="get")
@click.argument("user_id")
@click.option(
    "--fields",
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
def get_user(
    user_id: str,
    fields: str | None,
    authorizations: bool,
    output: str | None,
    api_login: str | None,
    api_password: str | None,
):
    """Get user details.

    Examples:
        sigfox users get 5138e7dfa2f1fffaf25fd409
        sigfox users get 5138e7dfa2f1fffaf25fd409 --authorizations
        sigfox users get 5138e7dfa2f1fffaf25fd409 --output json
    """
    try:
        client = get_sigfox_from_config(api_login, api_password)
        cfg = load_config()
        output_format = output or cfg.output_format

        with client:
            user = client.users.get(
                user_id, fields=fields, authorizations=authorizations
            )
            user_data = user.model_dump(by_alias=True)
            output_user_detail(user_data, output_format)

    except SigfoxCLIError as e:
        print_error(str(e))
        raise click.Abort()
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise click.Abort()


@users.command(name="create")
@click.option("--group-id", required=True, help="Group ID to associate the user to")
@click.option("--first-name", required=True, help="User's first name")
@click.option("--last-name", required=True, help="User's last name")
@click.option("--email", required=True, help="User's email address")
@click.option(
    "--timezone",
    required=True,
    help="Timezone (Java TimeZone ID, e.g., 'Europe/Paris')",
)
@click.option("--role-ids", required=True, help="Role IDs (comma-separated)")
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
def create_user(
    group_id: str,
    first_name: str,
    last_name: str,
    email: str,
    timezone: str,
    role_ids: str,
    output: str | None,
    api_login: str | None,
    api_password: str | None,
):
    """Create a new user.

    Examples:
        sigfox users create --group-id abc123 --first-name "John" \\
            --last-name "Doe" --email "john.doe@example.com" \\
            --timezone "Europe/Paris" --role-ids role1,role2
    """
    try:
        client = get_sigfox_from_config(api_login, api_password)
        cfg = load_config()
        output_format = output or cfg.output_format

        role_ids_list = [r.strip() for r in role_ids.split(",")]

        user_data = UserCreate(
            group_id=group_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            timezone=timezone,
            role_ids=role_ids_list,
        )

        with client:
            result = client.users.create(user_data)
            user_id = result.get("id", "unknown")
            print_success(f"User created successfully (ID: {user_id})")

            # Fetch and display the created user
            user = client.users.get(user_id)
            output_user_detail(user.model_dump(by_alias=True), output_format)

    except SigfoxCLIError as e:
        print_error(str(e))
        raise click.Abort()
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise click.Abort()


@users.command(name="update")
@click.argument("user_id")
@click.option("--first-name", help="User's first name")
@click.option("--last-name", help="User's last name")
@click.option("--email", help="User's email address")
@click.option("--timezone", help="Timezone (Java TimeZone ID)")
@click.option("--role-ids", help="Role IDs (comma-separated, replaces existing)")
@click.option("--api-login", envvar="SIGFOX_API_LOGIN", help="API login (ID)")
@click.option(
    "--api-password", envvar="SIGFOX_API_PASSWORD", help="API password (secret)"
)
def update_user(
    user_id: str,
    first_name: str | None,
    last_name: str | None,
    email: str | None,
    timezone: str | None,
    role_ids: str | None,
    api_login: str | None,
    api_password: str | None,
):
    """Update a user.

    Examples:
        sigfox users update 5138e7dfa2f1fffaf25fd409 --first-name "Jane"
        sigfox users update 5138e7dfa2f1fffaf25fd409 --email "new@example.com"
        sigfox users update 5138e7dfa2f1fffaf25fd409 --timezone "America/New_York"
        sigfox users update 5138e7dfa2f1fffaf25fd409 --role-ids role1,role2
    """
    try:
        client = get_sigfox_from_config(api_login, api_password)

        has_updates = any([
            first_name is not None,
            last_name is not None,
            email is not None,
            timezone is not None,
            role_ids is not None,
        ])

        if not has_updates:
            print_error(
                "No update fields specified. Use --first-name, --last-name, --email, --timezone, or --role-ids."
            )
            raise click.Abort()

        role_ids_list = (
            [r.strip() for r in role_ids.split(",")]
            if role_ids is not None
            else None
        )

        user_update = UserUpdate(
            first_name=first_name,
            last_name=last_name,
            email=email,
            timezone=timezone,
            role_ids=role_ids_list,
        )

        with client:
            client.users.update(user_id, user_update)
            print_success(f"User {user_id} updated successfully.")

    except SigfoxCLIError as e:
        print_error(str(e))
        raise click.Abort()
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise click.Abort()


@users.command(name="delete")
@click.argument("user_id")
@click.option(
    "--force", "-f", is_flag=True, default=False, help="Skip confirmation prompt"
)
@click.option("--api-login", envvar="SIGFOX_API_LOGIN", help="API login (ID)")
@click.option(
    "--api-password", envvar="SIGFOX_API_PASSWORD", help="API password (secret)"
)
def delete_user(
    user_id: str,
    force: bool,
    api_login: str | None,
    api_password: str | None,
):
    """Delete a user.

    Examples:
        sigfox users delete 5138e7dfa2f1fffaf25fd409
        sigfox users delete 5138e7dfa2f1fffaf25fd409 --force
    """
    try:
        if not force:
            click.confirm(
                f"Are you sure you want to delete user {user_id}?",
                abort=True,
            )

        client = get_sigfox_from_config(api_login, api_password)

        with client:
            client.users.delete(user_id)
            print_success(f"User {user_id} deleted successfully.")

    except click.Abort:
        raise
    except SigfoxCLIError as e:
        print_error(str(e))
        raise click.Abort()
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise click.Abort()


@users.command(name="add-roles")
@click.argument("user_id")
@click.option(
    "--role-ids", required=True, help="Role IDs to associate (comma-separated)"
)
@click.option("--api-login", envvar="SIGFOX_API_LOGIN", help="API login (ID)")
@click.option(
    "--api-password", envvar="SIGFOX_API_PASSWORD", help="API password (secret)"
)
def add_roles(
    user_id: str,
    role_ids: str,
    api_login: str | None,
    api_password: str | None,
):
    """Associate roles to a user.

    Examples:
        sigfox users add-roles 5138e7dfa2f1fffaf25fd409 --role-ids role1,role2
    """
    try:
        client = get_sigfox_from_config(api_login, api_password)
        role_ids_list = [r.strip() for r in role_ids.split(",")]

        with client:
            client.users.add_roles(user_id, role_ids_list)
            print_success(
                f"Roles associated to user {user_id} successfully."
            )

    except SigfoxCLIError as e:
        print_error(str(e))
        raise click.Abort()
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise click.Abort()


@users.command(name="remove-role")
@click.argument("user_id")
@click.argument("role_id")
@click.option(
    "--force", "-f", is_flag=True, default=False, help="Skip confirmation prompt"
)
@click.option("--api-login", envvar="SIGFOX_API_LOGIN", help="API login (ID)")
@click.option(
    "--api-password", envvar="SIGFOX_API_PASSWORD", help="API password (secret)"
)
def remove_role(
    user_id: str,
    role_id: str,
    force: bool,
    api_login: str | None,
    api_password: str | None,
):
    """Remove a role from a user.

    Examples:
        sigfox users remove-role 5138e7dfa2f1fffaf25fd409 role001
        sigfox users remove-role 5138e7dfa2f1fffaf25fd409 role001 --force
    """
    try:
        if not force:
            click.confirm(
                f"Are you sure you want to remove role {role_id} from user {user_id}?",
                abort=True,
            )

        client = get_sigfox_from_config(api_login, api_password)

        with client:
            client.users.remove_role(user_id, role_id)
            print_success(
                f"Role {role_id} removed from user {user_id} successfully."
            )

    except click.Abort:
        raise
    except SigfoxCLIError as e:
        print_error(str(e))
        raise click.Abort()
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise click.Abort()
