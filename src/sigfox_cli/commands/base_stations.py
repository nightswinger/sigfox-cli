"""Base station commands."""

import click

from . import get_sigfox_from_config
from ..config import load_config
from ..exceptions import SigfoxCLIError
from ..output import output_message_list, print_error, print_info


@click.group(name="base-stations")
def base_stations():
    """Manage Sigfox base stations."""
    pass


@base_stations.command(name="messages")
@click.argument("station_id")
@click.option(
    "--fields",
    help="Additional fields to return (e.g., 'device(name)', 'rinfos(baseStation(name))')",
)
@click.option("--since", type=int, help="Starting timestamp (milliseconds since Unix epoch)")
@click.option("--before", type=int, help="Ending timestamp (milliseconds since Unix epoch)")
@click.option("--limit", type=int, default=100, help="Maximum number of messages to fetch")
@click.option("--offset", type=int, default=0, help="Number of messages to skip")
@click.option(
    "--output",
    "-o",
    type=click.Choice(["table", "json"]),
    help="Output format",
)
@click.option("--api-login", envvar="SIGFOX_API_LOGIN", help="API login (ID)")
@click.option("--api-password", envvar="SIGFOX_API_PASSWORD", help="API password (secret)")
def list_messages(
    station_id: str,
    fields: str | None,
    since: int | None,
    before: int | None,
    limit: int,
    offset: int,
    output: str | None,
    api_login: str | None,
    api_password: str | None,
):
    """Retrieve messages received by a base station.

    The STATION_ID must be in hexadecimal format.

    Examples:
        sigfox base-stations messages 1A2B3C
        sigfox base-stations messages 1A2B3C --limit 50
        sigfox base-stations messages 1A2B3C --since 1609459200000 --before 1609545600000
        sigfox base-stations messages 1A2B3C --fields "device(name)"
        sigfox base-stations messages 1A2B3C --output json
    """
    try:
        client = get_sigfox_from_config(api_login, api_password)
        cfg = load_config()
        output_format = output or cfg.output_format

        with client:
            messages = client.base_stations.list_messages(
                station_id=station_id,
                fields=fields,
                since=since,
                before=before,
                limit=limit,
                offset=offset,
            )

            if not messages:
                print_info(f"No messages found for base station {station_id}.")
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
