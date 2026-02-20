"""Contract info commands."""

import click

from . import get_sigfox_from_config
from ..config import load_config
from ..exceptions import SigfoxCLIError
from ..output import (
    output_contract_info_detail,
    output_contract_info_list,
    output_device_list,
    print_error,
    print_info,
)


@click.group(name="contract-infos")
def contract_infos():
    """Manage Sigfox contract infos (subscriptions)."""
    pass


@contract_infos.command(name="list")
@click.option("--limit", type=int, default=100, help="Maximum number of contracts to fetch")
@click.option("--offset", type=int, default=0, help="Number of contracts to skip")
@click.option("--name", help="Filter by contract name (substring match)")
@click.option("--group-id", help="Filter by group ID")
@click.option("--group-type", type=int, help="Filter by group type (2=BASIC, 9=CHANNEL)")
@click.option("--deep", is_flag=True, default=False, help="Include contracts from child groups")
@click.option("--up", is_flag=True, default=False, help="Include contracts from ancestor groups")
@click.option("--order-ids", help="Filter by order IDs (comma-separated)")
@click.option("--contract-ids", help="Filter by external contract IDs (comma-separated)")
@click.option("--subscription-plan", type=int, help="Filter by subscription plan (0-6)")
@click.option("--pricing-model", type=int, help="Filter by pricing model (1-3)")
@click.option("--fields", help="Additional fields to return")
@click.option(
    "--authorizations",
    is_flag=True,
    default=False,
    help="Return actions and resources",
)
@click.option(
    "--output", "-o", type=click.Choice(["table", "json"]), help="Output format"
)
@click.option("--api-login", envvar="SIGFOX_API_LOGIN", help="API login (ID)")
@click.option("--api-password", envvar="SIGFOX_API_PASSWORD", help="API password (secret)")
def list_contract_infos(
    limit: int,
    offset: int,
    name: str | None,
    group_id: str | None,
    group_type: int | None,
    deep: bool,
    up: bool,
    order_ids: str | None,
    contract_ids: str | None,
    subscription_plan: int | None,
    pricing_model: int | None,
    fields: str | None,
    authorizations: bool,
    output: str | None,
    api_login: str | None,
    api_password: str | None,
):
    """List contract infos.

    Examples:
        sigfox contract-infos list
        sigfox contract-infos list --limit 50
        sigfox contract-infos list --group-id abc123
        sigfox contract-infos list --subscription-plan 1
        sigfox contract-infos list --output json
    """
    try:
        client = get_sigfox_from_config(api_login, api_password)
        cfg = load_config()
        output_format = output or cfg.output_format

        with client:
            result = client.contract_infos.list(
                limit=limit,
                offset=offset,
                name=name,
                group_id=group_id,
                group_type=group_type,
                deep=deep,
                up=up,
                order_ids=order_ids,
                contract_ids=contract_ids,
                subscription_plan=subscription_plan,
                pricing_model=pricing_model,
                fields=fields,
                authorizations=authorizations,
            )

            if not result:
                print_info("No contract infos found.")
                return

            data = [c.model_dump(by_alias=True) for c in result]
            output_contract_info_list(data, output_format)

    except SigfoxCLIError as e:
        print_error(str(e))
        raise click.Abort()
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise click.Abort()


@contract_infos.command(name="get")
@click.argument("contract_id")
@click.option("--fields", help="Additional fields to return")
@click.option(
    "--authorizations",
    is_flag=True,
    default=False,
    help="Return actions and resources",
)
@click.option(
    "--output", "-o", type=click.Choice(["table", "json"]), help="Output format"
)
@click.option("--api-login", envvar="SIGFOX_API_LOGIN", help="API login (ID)")
@click.option("--api-password", envvar="SIGFOX_API_PASSWORD", help="API password (secret)")
def get_contract_info(
    contract_id: str,
    fields: str | None,
    authorizations: bool,
    output: str | None,
    api_login: str | None,
    api_password: str | None,
):
    """Get contract info details.

    Examples:
        sigfox contract-infos get 572f1204017975032d8ec1dd
        sigfox contract-infos get 572f1204017975032d8ec1dd --authorizations
        sigfox contract-infos get 572f1204017975032d8ec1dd --output json
    """
    try:
        client = get_sigfox_from_config(api_login, api_password)
        cfg = load_config()
        output_format = output or cfg.output_format

        with client:
            contract = client.contract_infos.get(
                contract_id, fields=fields, authorizations=authorizations
            )
            output_contract_info_detail(contract.model_dump(by_alias=True), output_format)

    except SigfoxCLIError as e:
        print_error(str(e))
        raise click.Abort()
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise click.Abort()


@contract_infos.command(name="list-devices")
@click.argument("contract_id")
@click.option("--device-type-id", help="Filter by device type ID")
@click.option("--fields", help="Additional fields to return")
@click.option("--limit", type=int, default=100, help="Maximum number of devices to fetch")
@click.option(
    "--output", "-o", type=click.Choice(["table", "json"]), help="Output format"
)
@click.option("--api-login", envvar="SIGFOX_API_LOGIN", help="API login (ID)")
@click.option("--api-password", envvar="SIGFOX_API_PASSWORD", help="API password (secret)")
def list_devices(
    contract_id: str,
    device_type_id: str | None,
    fields: str | None,
    limit: int,
    output: str | None,
    api_login: str | None,
    api_password: str | None,
):
    """List devices with a token on the specified contract.

    Examples:
        sigfox contract-infos list-devices 572f1204017975032d8ec1dd
        sigfox contract-infos list-devices 572f1204017975032d8ec1dd --limit 50
        sigfox contract-infos list-devices 572f1204017975032d8ec1dd --output json
    """
    try:
        client = get_sigfox_from_config(api_login, api_password)
        cfg = load_config()
        output_format = output or cfg.output_format

        with client:
            devices = client.contract_infos.list_devices(
                contract_id,
                device_type_id=device_type_id,
                fields=fields,
                limit=limit,
            )

            if not devices:
                print_info("No devices found for this contract.")
                return

            output_device_list(devices, output_format)

    except SigfoxCLIError as e:
        print_error(str(e))
        raise click.Abort()
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise click.Abort()
