"""Profile commands."""

import click

from . import get_sigfox_from_config
from ..config import load_config
from ..exceptions import SigfoxCLIError
from ..output import (
    output_json,
    output_profile_detail,
    output_profile_list,
    print_error,
    print_info,
)


@click.group(name="profiles")
def profiles():
    """Manage Sigfox profiles."""
    pass


@profiles.command(name="list")
@click.option(
    "--group-id",
    required=True,
    help="Group ID to list profiles for",
)
@click.option(
    "--inherit",
    is_flag=True,
    default=False,
    help="Also return profiles inherited from parent's group",
)
@click.option(
    "--limit", type=int, default=100, help="Maximum number of profiles to fetch"
)
@click.option("--offset", type=int, default=0, help="Number of profiles to skip")
@click.option(
    "--fields",
    help="Additional fields to return",
)
@click.option(
    "--authorizations",
    is_flag=True,
    default=False,
    help="Return profile's actions and resources",
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
def list_profiles(
    group_id: str,
    inherit: bool,
    limit: int,
    offset: int,
    fields: str | None,
    authorizations: bool,
    output: str | None,
    api_login: str | None,
    api_password: str | None,
):
    """List profiles.

    Examples:
        sigfox profiles list --group-id abc123
        sigfox profiles list --group-id abc123 --inherit
        sigfox profiles list --group-id abc123 --output json
    """
    try:
        client = get_sigfox_from_config(api_login, api_password)
        cfg = load_config()
        output_format = output or cfg.output_format

        with client:
            result = client.profiles.list(
                group_id=group_id,
                inherit=inherit,
                fields=fields,
                limit=limit,
                offset=offset,
                authorizations=authorizations,
            )

            if not result:
                print_info("No profiles found.")
                return

            data = [p.model_dump(by_alias=True) for p in result]
            output_profile_list(data, output_format)

    except SigfoxCLIError as e:
        print_error(str(e))
        raise click.Abort()
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise click.Abort()


@profiles.command(name="get")
@click.argument("profile_id")
@click.option(
    "--fields",
    help="Additional fields to return",
)
@click.option(
    "--authorizations",
    is_flag=True,
    default=False,
    help="Return profile's actions and resources",
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
def get_profile(
    profile_id: str,
    fields: str | None,
    authorizations: bool,
    output: str | None,
    api_login: str | None,
    api_password: str | None,
):
    """Get profile details.

    Examples:
        sigfox profiles get 572f71a08916342398fb65c5
        sigfox profiles get 572f71a08916342398fb65c5 --authorizations
        sigfox profiles get 572f71a08916342398fb65c5 --output json
    """
    try:
        client = get_sigfox_from_config(api_login, api_password)
        cfg = load_config()
        output_format = output or cfg.output_format

        with client:
            profile = client.profiles.get(
                profile_id, fields=fields, authorizations=authorizations
            )
            profile_data = profile.model_dump(by_alias=True)
            output_profile_detail(profile_data, output_format)

    except SigfoxCLIError as e:
        print_error(str(e))
        raise click.Abort()
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise click.Abort()
