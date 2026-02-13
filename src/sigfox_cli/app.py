"""Main CLI application."""

import click

from .commands import config_cmd, device_types, devices, groups


@click.group()
@click.version_option(version="0.1.0", prog_name="sigfox")
def cli():
    """Sigfox CLI - Command-line tool for Sigfox API v2."""
    pass


# Register command groups
cli.add_command(config_cmd.config)
cli.add_command(devices.devices)
cli.add_command(device_types.device_types)
cli.add_command(groups.groups)


if __name__ == "__main__":
    cli()
