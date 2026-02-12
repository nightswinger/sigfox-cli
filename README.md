# sigfox-cli

Command-line interface for Sigfox API v2. Manage Sigfox devices and retrieve messages with ease.

## Features

- 🔐 Secure configuration management (environment variables, config file)
- 📱 Device management (list, get details)
- 📨 Message retrieval with filtering
- 📊 Multiple output formats (table, JSON)
- 🎨 Beautiful terminal output with rich

## Installation

### Prerequisites

- Python 3.13 or higher
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Using uv

```bash
uv sync
```

### Using pip

```bash
pip install -e .
```

## Configuration

### Interactive Setup

The easiest way to configure sigfox-cli:

```bash
sigfox config init
```

This will prompt you for:
- API Login (ID)
- API Password (Secret)
- API Base URL (default: https://api.sigfox.com/v2)
- Default output format (table or json)
- Request timeout

### Environment Variables

You can also set credentials via environment variables:

```bash
export SIGFOX_API_LOGIN="your_api_login"
export SIGFOX_API_PASSWORD="your_api_password"
```

### Configuration File

Configuration is stored at `~/.config/sigfox-cli/config.toml`:

```toml
[auth]
api_login = "xxxxxxxxxxxxxxxxxxxxxxxx"
api_password = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

[api]
base_url = "https://api.sigfox.com/v2"
timeout = 30

[output]
default_format = "table"
```

### Configuration Priority

1. Command-line arguments (`--api-login`, `--api-password`)
2. Environment variables (`SIGFOX_API_LOGIN`, `SIGFOX_API_PASSWORD`)
3. Configuration file (`~/.config/sigfox-cli/config.toml`)

## Usage

### Configuration Commands

```bash
# Initialize configuration
sigfox config init

# Show current configuration
sigfox config show

# Set individual configuration values
sigfox config set api_login YOUR_LOGIN
sigfox config set output_format json
```

### Device Commands

```bash
# List devices (default: 100 devices, table format)
sigfox devices list

# List with options
sigfox devices list --limit 50 --offset 10
sigfox devices list --device-type-id 5d8cdc8fea06bb6e41234567
sigfox devices list --group-ids abc123,def456 --deep  # Search in groups and subgroups
sigfox devices list --output json

# Get device details
sigfox devices get 1A2B3C
sigfox devices get 1A2B3C --output json

# List messages for a device
sigfox devices messages 1A2B3C
sigfox devices messages 1A2B3C --limit 50
sigfox devices messages 1A2B3C --since 1609459200000 --before 1609545600000
sigfox devices messages 1A2B3C --output json
```

### Common Options

- `--output, -o`: Output format (`table` or `json`)
- `--api-login`: Override API login
- `--api-password`: Override API password

## Examples

### List all devices in table format

```bash
sigfox devices list
```

Output:
```
                                    Devices
┏━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┓
┃ ID     ┃ Name       ┃ Device Type  ┃ State ┃ Last Com            ┃ PAC       ┃
┡━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━┩
│ 1A2B3C │ Device #1  │ Type A       │ 0     │ 2024-01-15 10:30:45 │ ABC123... │
│ 4D5E6F │ Device #2  │ Type B       │ 0     │ 2024-01-15 09:15:22 │ DEF456... │
└────────┴────────────┴──────────────┴───────┴─────────────────────┴───────────┘
```

### Get device details in JSON format

```bash
sigfox devices get 1A2B3C --output json
```

### List recent messages

```bash
sigfox devices messages 1A2B3C --limit 10
```

## Development

### Install Development Dependencies

```bash
uv sync
```

### Run Tests

```bash
uv run pytest
```

### Type Checking

```bash
uv run mypy src/sigfox_cli
```

### Project Structure

```
sigfox-cli/
├── src/
│   └── sigfox_cli/
│       ├── __init__.py
│       ├── app.py              # Main CLI application
│       ├── client.py           # Sigfox API client
│       ├── config.py           # Configuration management
│       ├── exceptions.py       # Custom exceptions
│       ├── output.py           # Output formatting
│       ├── commands/
│       │   ├── config_cmd.py   # Config commands
│       │   └── devices.py      # Device commands
│       └── models/
│           ├── device.py       # Device models
│           └── message.py      # Message models
├── tests/
└── pyproject.toml
```

## API Reference

This CLI interacts with [Sigfox API v2](https://support.sigfox.com/apidocs).

### Authentication

Uses HTTP Basic Authentication with:
- API Login (ID)
- API Password (Secret)

### Endpoints Supported

- `GET /devices/` - List devices
- `GET /devices/{id}` - Get device details
- `GET /devices/{id}/messages` - List device messages

## Troubleshooting

### Authentication Errors

If you see "Authentication failed":
1. Check your API credentials in `sigfox config show`
2. Verify credentials are correct in the Sigfox Backend
3. Ensure you have necessary permissions

### Network Errors

If you see "Network error" or "Request timeout":
1. Check your internet connection
2. Verify the API base URL is correct
3. Try increasing the timeout: `sigfox config set timeout 60`

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
