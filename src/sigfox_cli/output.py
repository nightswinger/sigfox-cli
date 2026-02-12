"""Output formatting utilities."""

import json
from datetime import datetime
from typing import Any

from rich.console import Console
from rich.json import JSON
from rich.table import Table


console = Console()


def format_timestamp(timestamp_ms: int | None) -> str:
    """Format Unix timestamp (milliseconds) to human-readable string.

    Args:
        timestamp_ms: Timestamp in milliseconds since Unix epoch

    Returns:
        Formatted date-time string or "-" if None
    """
    if timestamp_ms is None:
        return "-"
    try:
        dt = datetime.fromtimestamp(timestamp_ms / 1000)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except (ValueError, OSError):
        return str(timestamp_ms)


def format_hex(hex_str: str | None, max_length: int = 32) -> str:
    """Format hex string with truncation.

    Args:
        hex_str: Hex string
        max_length: Maximum length before truncation

    Returns:
        Formatted hex string
    """
    if hex_str is None:
        return "-"
    if len(hex_str) > max_length:
        return f"{hex_str[:max_length]}..."
    return hex_str


def output_json(data: Any) -> None:
    """Output data as formatted JSON.

    Args:
        data: Data to output
    """
    if isinstance(data, str):
        console.print(data)
    else:
        json_str = json.dumps(data, indent=2, ensure_ascii=False)
        console.print(JSON(json_str))


def output_table(
    data: list[dict[str, Any]],
    columns: list[tuple[str, str]],
    title: str | None = None,
) -> None:
    """Output data as a table.

    Args:
        data: List of data items
        columns: List of (header, key) tuples defining table columns
        title: Optional table title
    """
    if not data:
        console.print("[dim]No data to display[/dim]")
        return

    table = Table(title=title, show_header=True, header_style="bold cyan")

    # Add columns
    for header, _ in columns:
        table.add_column(header)

    # Add rows
    for item in data:
        row = []
        for _, key in columns:
            # Support nested keys with dot notation (e.g., "device.name")
            value = item
            for k in key.split("."):
                value = value.get(k) if isinstance(value, dict) else None
                if value is None:
                    break

            # Format value based on type
            if value is None:
                row.append("-")
            elif isinstance(value, bool):
                row.append("✓" if value else "✗")
            elif isinstance(value, int) and key.endswith("Time"):
                # Format timestamps
                row.append(format_timestamp(value))
            elif isinstance(value, str) and len(value) > 50:
                # Truncate long strings
                row.append(f"{value[:50]}...")
            else:
                row.append(str(value))

        table.add_row(*row)

    console.print(table)


def output_device_list(devices: list[dict[str, Any]], output_format: str = "table") -> None:
    """Output device list in specified format.

    Args:
        devices: List of device data
        output_format: Output format ("table" or "json")
    """
    if output_format == "json":
        output_json(devices)
    else:
        columns = [
            ("ID", "id"),
            ("Name", "name"),
            ("Device Type", "deviceType.name"),
            ("State", "state"),
            ("Last Com", "lastCom"),
            ("PAC", "pac"),
        ]
        output_table(devices, columns, title="Devices")


def output_device_detail(device: dict[str, Any], output_format: str = "table") -> None:
    """Output device details in specified format.

    Args:
        device: Device data
        output_format: Output format ("table" or "json")
    """
    if output_format == "json":
        output_json(device)
    else:
        # Create a two-column table for key-value pairs
        table = Table(show_header=False, title="Device Details")
        table.add_column("Property", style="bold cyan")
        table.add_column("Value")

        # Selected fields to display
        fields = [
            ("ID", "id"),
            ("Name", "name"),
            ("Device Type", "deviceType.name"),
            ("State", "state"),
            ("Com State", "comState"),
            ("Last Com", "lastCom"),
            ("Creation Time", "creationTime"),
            ("Activation Time", "activationTime"),
            ("PAC", "pac"),
            ("Sequence Number", "sequenceNumber"),
            ("LQI", "lqi"),
            ("Satellite Capable", "satelliteCapable"),
            ("Repeater", "repeater"),
            ("Automatic Renewal", "automaticRenewal"),
        ]

        for label, key in fields:
            value = device
            for k in key.split("."):
                value = value.get(k) if isinstance(value, dict) else None
                if value is None:
                    break

            if value is None:
                continue

            # Format value
            if isinstance(value, bool):
                formatted_value = "✓ Yes" if value else "✗ No"
            elif isinstance(value, int) and key.endswith("Time"):
                formatted_value = format_timestamp(value)
            else:
                formatted_value = str(value)

            table.add_row(label, formatted_value)

        console.print(table)


def output_message_list(messages: list[dict[str, Any]], output_format: str = "table") -> None:
    """Output message list in specified format.

    Args:
        messages: List of message data
        output_format: Output format ("table" or "json")
    """
    if output_format == "json":
        output_json(messages)
    else:
        columns = [
            ("Time", "time"),
            ("Device", "device.id"),
            ("Data", "data"),
            ("Seq#", "seqNumber"),
            ("LQI", "lqi"),
            ("Frames", "nbFrames"),
        ]
        output_table(messages, columns, title="Messages")


def print_success(message: str) -> None:
    """Print success message.

    Args:
        message: Success message
    """
    console.print(f"[green]✓[/green] {message}")


def print_error(message: str) -> None:
    """Print error message.

    Args:
        message: Error message
    """
    console.print(f"[red]✗[/red] {message}", err=True)


def print_warning(message: str) -> None:
    """Print warning message.

    Args:
        message: Warning message
    """
    console.print(f"[yellow]⚠[/yellow] {message}")


def print_info(message: str) -> None:
    """Print info message.

    Args:
        message: Info message
    """
    console.print(f"[blue]ℹ[/blue] {message}")
