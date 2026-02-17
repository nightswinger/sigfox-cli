"""Main CLI application."""

import click

from .commands import api_users, base_stations, config_cmd, device_types, devices, groups, users


@click.group()
@click.version_option(version="0.1.0", prog_name="sigfox")
def cli():
    """Sigfox CLI - Command-line tool for Sigfox API v2."""
    pass


# Register command groups
cli.add_command(api_users.api_users)
cli.add_command(base_stations.base_stations)
cli.add_command(config_cmd.config)
cli.add_command(devices.devices)
cli.add_command(device_types.device_types)
cli.add_command(groups.groups)
cli.add_command(users.users)


if __name__ == "__main__":
    cli()
