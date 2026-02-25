"""Operator commands."""

import click

from . import get_sigfox_from_config
from ..config import load_config
from ..exceptions import SigfoxCLIError
from ..output import (
    output_json,
    output_operator_detail,
    output_operator_list,
    print_error,
    print_info,
)


@click.group(name="operators")
def operators():
    """Manage Sigfox operators (network operators)."""
    pass


@operators.command(name="list")
@click.option(
    "--limit", type=int, default=100, help="Maximum number of operators to fetch"
)
@click.option("--offset", type=int, default=0, help="Number of operators to skip")
@click.option("--group-ids", help="Filter by group IDs (comma-separated)")
@click.option(
    "--deep",
    is_flag=True,
    default=False,
    help="Include operators from all child groups",
)
@click.option(
    "--fields",
    help="Additional fields to return",
)
@click.option(
    "--authorizations",
    is_flag=True,
    default=False,
    help="Return operator's actions and resources",
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
def list_operators(
    limit: int,
    offset: int,
    group_ids: str | None,
    deep: bool,
    fields: str | None,
    authorizations: bool,
    output: str | None,
    api_login: str | None,
    api_password: str | None,
):
    """List operators.

    Examples:
        sigfox operators list
        sigfox operators list --limit 50
        sigfox operators list --group-ids abc123,def456
        sigfox operators list --deep
        sigfox operators list --output json
    """
    try:
        client = get_sigfox_from_config(api_login, api_password)
        cfg = load_config()
        output_format = output or cfg.output_format

        group_ids_list = group_ids.split(",") if group_ids else None

        with client:
            result = client.operators.list(
                limit=limit,
                offset=offset,
                group_ids=group_ids_list,
                deep=deep,
                fields=fields,
                authorizations=authorizations,
            )

            if not result:
                print_info("No operators found.")
                return

            data = [o.model_dump(by_alias=True) for o in result]
            output_operator_list(data, output_format)

    except SigfoxCLIError as e:
        print_error(str(e))
        raise click.Abort()
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise click.Abort()


@operators.command(name="get")
@click.argument("operator_id")
@click.option(
    "--fields",
    help="Additional fields to return",
)
@click.option(
    "--authorizations",
    is_flag=True,
    default=False,
    help="Return operator's actions and resources",
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
def get_operator(
    operator_id: str,
    fields: str | None,
    authorizations: bool,
    output: str | None,
    api_login: str | None,
    api_password: str | None,
):
    """Get operator details.

    Examples:
        sigfox operators get 5138e7dfa2f1fffaf25fd409
        sigfox operators get 5138e7dfa2f1fffaf25fd409 --authorizations
        sigfox operators get 5138e7dfa2f1fffaf25fd409 --output json
    """
    try:
        client = get_sigfox_from_config(api_login, api_password)
        cfg = load_config()
        output_format = output or cfg.output_format

        with client:
            operator = client.operators.get(
                operator_id, fields=fields, authorizations=authorizations
            )
            operator_data = operator.model_dump(by_alias=True)
            output_operator_detail(operator_data, output_format)

    except SigfoxCLIError as e:
        print_error(str(e))
        raise click.Abort()
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise click.Abort()
