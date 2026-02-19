"""Coverage commands."""

import json
from typing import Any

import click
from sigfox.models import CoverageBulkRequest, CoverageLocation

from . import get_sigfox_from_config
from ..config import load_config
from ..exceptions import ConfigError, SigfoxCLIError
from ..output import (
    output_coverage_bulk_response,
    output_coverage_prediction,
    output_coverage_redundancy,
    print_error,
    print_info,
)


@click.group(name="coverages")
def coverages():
    """Query Sigfox coverage predictions."""
    pass


@coverages.command(name="global-prediction")
@click.option("--lat", required=True, type=float, help="Latitude in degrees (WGS 84)")
@click.option("--lng", required=True, type=float, help="Longitude in degrees (WGS 84)")
@click.option("--radius", type=int, help="Estimated radius of the device location (meters)")
@click.option("--group-id", help="Filter by group ID")
@click.option(
    "--output", "-o",
    type=click.Choice(["table", "json"]),
    help="Output format",
)
@click.option("--api-login", envvar="SIGFOX_API_LOGIN", help="API login (ID)")
@click.option("--api-password", envvar="SIGFOX_API_PASSWORD", help="API password (secret)")
def global_prediction(
    lat: float,
    lng: float,
    radius: int | None,
    group_id: str | None,
    output: str | None,
    api_login: str | None,
    api_password: str | None,
):
    """Get coverage prediction for a single location.

    Examples:
        sigfox coverages global-prediction --lat 48.8566 --lng 2.3522
        sigfox coverages global-prediction --lat 48.8566 --lng 2.3522 --radius 100
        sigfox coverages global-prediction --lat 48.8566 --lng 2.3522 --output json
    """
    try:
        client = get_sigfox_from_config(api_login, api_password)
        cfg = load_config()
        output_format = output or cfg.output_format

        with client:
            result = client.coverages.get_global_prediction(
                lat=lat,
                lng=lng,
                radius=radius,
                group_id=group_id,
            )
            output_coverage_prediction(result.model_dump(by_alias=True), output_format)

    except SigfoxCLIError as e:
        print_error(str(e))
        raise click.Abort()
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise click.Abort()


@coverages.command(name="bulk-start")
@click.option(
    "--locations",
    required=True,
    help='JSON array of locations, e.g. \'[{"lat": 48.86, "lng": 2.35}]\'',
)
@click.option("--radius", type=int, help="Estimated radius of the device location (meters)")
@click.option("--group-id", help="Filter by group ID")
@click.option("--api-login", envvar="SIGFOX_API_LOGIN", help="API login (ID)")
@click.option("--api-password", envvar="SIGFOX_API_PASSWORD", help="API password (secret)")
def bulk_start(
    locations: str,
    radius: int | None,
    group_id: str | None,
    api_login: str | None,
    api_password: str | None,
):
    """Start a bulk coverage prediction job for multiple locations.

    Examples:
        sigfox coverages bulk-start --locations '[{"lat": 48.86, "lng": 2.35}]'
        sigfox coverages bulk-start --locations '[{"lat": 48.86, "lng": 2.35}, {"lat": 51.51, "lng": -0.13}]'
    """
    try:
        locations_data: list[dict[str, Any]] = json.loads(locations)
        location_objs = [CoverageLocation(lat=loc["lat"], lng=loc["lng"]) for loc in locations_data]
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        print_error(f"Invalid --locations JSON: {e}")
        raise click.Abort()

    try:
        client = get_sigfox_from_config(api_login, api_password)

        request = CoverageBulkRequest(
            locations=location_objs,
            radius=radius,
            group_id=group_id,
        )

        with client:
            result = client.coverages.start_bulk_prediction(request)
            job_id = result.get("jobId", "unknown")
            click.echo(f"Bulk job started. Job ID: {job_id}")
            click.echo(f"Run: sigfox coverages bulk-get {job_id}")

    except SigfoxCLIError as e:
        print_error(str(e))
        raise click.Abort()
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise click.Abort()


@coverages.command(name="bulk-get")
@click.argument("job_id")
@click.option(
    "--output", "-o",
    type=click.Choice(["table", "json"]),
    help="Output format",
)
@click.option("--api-login", envvar="SIGFOX_API_LOGIN", help="API login (ID)")
@click.option("--api-password", envvar="SIGFOX_API_PASSWORD", help="API password (secret)")
def bulk_get(
    job_id: str,
    output: str | None,
    api_login: str | None,
    api_password: str | None,
):
    """Get results of a bulk coverage prediction job.

    Examples:
        sigfox coverages bulk-get <job_id>
        sigfox coverages bulk-get <job_id> --output json
    """
    try:
        client = get_sigfox_from_config(api_login, api_password)
        cfg = load_config()
        output_format = output or cfg.output_format

        with client:
            result = client.coverages.get_bulk_prediction(job_id)
            output_coverage_bulk_response(result.model_dump(by_alias=True), output_format)

    except SigfoxCLIError as e:
        print_error(str(e))
        raise click.Abort()
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise click.Abort()


@coverages.command(name="operator-redundancy")
@click.option("--lat", required=True, type=float, help="Latitude in degrees (WGS 84)")
@click.option("--lng", required=True, type=float, help="Longitude in degrees (WGS 84)")
@click.option("--operator-id", help="Operator group ID (required for root Sigfox users)")
@click.option(
    "--device-situation",
    type=click.Choice(["OUTDOOR", "INDOOR", "UNDERGROUND"]),
    help="Device installation context",
)
@click.option("--device-class-id", type=int, help="Sigfox device class (0u, 1u, 2u, 3u)")
@click.option(
    "--output", "-o",
    type=click.Choice(["table", "json"]),
    help="Output format",
)
@click.option("--api-login", envvar="SIGFOX_API_LOGIN", help="API login (ID)")
@click.option("--api-password", envvar="SIGFOX_API_PASSWORD", help="API password (secret)")
def operator_redundancy(
    lat: float,
    lng: float,
    operator_id: str | None,
    device_situation: str | None,
    device_class_id: int | None,
    output: str | None,
    api_login: str | None,
    api_password: str | None,
):
    """Get operator redundancy coverage for a location.

    Examples:
        sigfox coverages operator-redundancy --lat 48.8566 --lng 2.3522
        sigfox coverages operator-redundancy --lat 48.8566 --lng 2.3522 --device-situation OUTDOOR
        sigfox coverages operator-redundancy --lat 48.8566 --lng 2.3522 --operator-id abc123
        sigfox coverages operator-redundancy --lat 48.8566 --lng 2.3522 --output json
    """
    try:
        client = get_sigfox_from_config(api_login, api_password)
        cfg = load_config()
        output_format = output or cfg.output_format

        with client:
            result = client.coverages.get_operator_redundancy(
                lat=lat,
                lng=lng,
                operator_id=operator_id,
                device_situation=device_situation,
                device_class_id=device_class_id,
            )
            output_coverage_redundancy(result.model_dump(by_alias=True), output_format)

    except SigfoxCLIError as e:
        print_error(str(e))
        raise click.Abort()
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        raise click.Abort()
