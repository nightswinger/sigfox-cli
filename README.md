# sigfox-cli

Command-line interface for Sigfox API v2. Manage Sigfox devices and retrieve messages with ease.

## Features

- 🔐 Secure configuration management (environment variables, config file)
- 📱 Device management (list, get, create, update, delete)
- 🔧 Device type management (list, get, create, update, delete)
- 📡 Base station message retrieval
- 🗺️ Coverage predictions (single location, bulk, operator redundancy)
- 📁 Group management (list, get, create, update, delete, callbacks, geolocation)
- 🔑 API user management (list, get, create, update, delete, profiles, credentials)
- 🏢 Operator management (list, get)
- 👤 User management (list, get, create, update, delete, roles)
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

# Create a new device
sigfox devices create --device-id 1A2B3C --name "My Device" --device-type-id 5d8cdc8fea06bb6e41234567 --pac ABC123DEF456
sigfox devices create --device-id 1A2B3C --name "Test Device" --device-type-id 5d8cdc8fea06bb6e41234567 --pac ABC123 --lat 48.8585715 --lng 2.2922923
sigfox devices create --device-id 1A2B3C --name "Prototype" --device-type-id 5d8cdc8fea06bb6e41234567 --pac ABC123 --prototype

# Update a device
sigfox devices update 1A2B3C --name "New Name"
sigfox devices update 1A2B3C --lat 48.8585715 --lng 2.2922923
sigfox devices update 1A2B3C --prototype true --automatic-renewal false

# Delete a device (with confirmation prompt)
sigfox devices delete 1A2B3C

# Delete a device (skip confirmation)
sigfox devices delete 1A2B3C --force

# List messages for a device
sigfox devices messages 1A2B3C
sigfox devices messages 1A2B3C --limit 50
sigfox devices messages 1A2B3C --since 1609459200000 --before 1609545600000
sigfox devices messages 1A2B3C --output json
```

### Device Type Commands

```bash
# List device types (default: 100 device types, table format)
sigfox device-types list

# List with options
sigfox device-types list --limit 50 --offset 10
sigfox device-types list --name MyType  # Filter by name prefix
sigfox device-types list --group-ids abc123,def456 --deep  # Search in groups and subgroups
sigfox device-types list --contract-id xyz789
sigfox device-types list --output json

# Get device type details
sigfox device-types get 5d8cdc8fea06bb6e41234567
sigfox device-types get 5d8cdc8fea06bb6e41234567 --output json

# Create a new device type
sigfox device-types create --name "My Device Type" --group-id abc123
sigfox device-types create --name "My Type" --group-id abc123 --description "Production sensors"
sigfox device-types create --name "My Type" --group-id abc123 --keep-alive 3600 --payload-type 2

# Update a device type
sigfox device-types update 5d8cdc8fea06bb6e41234567 --name "Updated Name"
sigfox device-types update 5d8cdc8fea06bb6e41234567 --description "New description" --keep-alive 7200

# Delete a device type (with confirmation prompt)
sigfox device-types delete 5d8cdc8fea06bb6e41234567

# Delete a device type (skip confirmation)
sigfox device-types delete 5d8cdc8fea06bb6e41234567 --force
```

### Coverage Commands

```bash
# Get coverage prediction for a single location
sigfox coverages global-prediction --lat 48.8566 --lng 2.3522
sigfox coverages global-prediction --lat 48.8566 --lng 2.3522 --radius 100
sigfox coverages global-prediction --lat 48.8566 --lng 2.3522 --group-id abc123
sigfox coverages global-prediction --lat 48.8566 --lng 2.3522 --output json

# Start a bulk coverage prediction job (async)
sigfox coverages bulk-start --locations '[{"lat": 48.86, "lng": 2.35}]'
sigfox coverages bulk-start --locations '[{"lat": 48.86, "lng": 2.35}, {"lat": 51.51, "lng": -0.13}]'
sigfox coverages bulk-start --locations '[{"lat": 48.86, "lng": 2.35}]' --radius 200

# Get results of a bulk prediction job
sigfox coverages bulk-get <job_id>
sigfox coverages bulk-get <job_id> --output json

# Get operator redundancy coverage for a location
sigfox coverages operator-redundancy --lat 48.8566 --lng 2.3522
sigfox coverages operator-redundancy --lat 48.8566 --lng 2.3522 --device-situation OUTDOOR
sigfox coverages operator-redundancy --lat 48.8566 --lng 2.3522 --device-situation INDOOR --device-class-id 0
sigfox coverages operator-redundancy --lat 48.8566 --lng 2.3522 --operator-id abc123
sigfox coverages operator-redundancy --lat 48.8566 --lng 2.3522 --output json
```

### Base Station Commands

```bash
# List messages received by a base station
sigfox base-stations messages 1A2B3C
sigfox base-stations messages 1A2B3C --limit 50
sigfox base-stations messages 1A2B3C --since 1609459200000 --before 1609545600000
sigfox base-stations messages 1A2B3C --fields "device(name)"
sigfox base-stations messages 1A2B3C --output json
```

### Group Commands

```bash
# List groups (default: 100 groups, table format)
sigfox groups list

# List with options
sigfox groups list --limit 50 --offset 10
sigfox groups list --parent-ids abc123,def456 --deep  # Search in groups and subgroups
sigfox groups list --name "My Group"
sigfox groups list --types 0,2,8  # Filter by type (0=SO, 2=Other, 5=SVNO, 8=DIST, etc.)
sigfox groups list --sort name
sigfox groups list --action "devices:create"  # Filter by allowed action
sigfox groups list --output json

# Get group details
sigfox groups get 572f1204017975032d8ec1dd
sigfox groups get 572f1204017975032d8ec1dd --authorizations
sigfox groups get 572f1204017975032d8ec1dd --output json

# Create a new group
sigfox groups create --name "My Group" --description "Test group" --type 8 --timezone "Europe/Paris" --parent-id abc123
sigfox groups create --name "SVNO Group" --description "SVNO" --type 5 --timezone "Europe/Paris" --parent-id abc123 --network-operator-id def456

# Update a group
sigfox groups update 572f1204017975032d8ec1dd --name "New Name"
sigfox groups update 572f1204017975032d8ec1dd --description "Updated desc" --timezone "America/New_York"

# Delete a group (with confirmation prompt)
sigfox groups delete 572f1204017975032d8ec1dd

# Delete a group (skip confirmation)
sigfox groups delete 572f1204017975032d8ec1dd --force

# List undelivered callbacks for a group
sigfox groups callbacks-not-delivered abc123
sigfox groups callbacks-not-delivered abc123 --since 1609459200000 --before 1609545600000
sigfox groups callbacks-not-delivered abc123 --limit 50

# List geolocation payloads for a group
sigfox groups geoloc-payloads abc123
sigfox groups geoloc-payloads abc123 --limit 50
sigfox groups geoloc-payloads abc123 --output json
```

### API User Commands

```bash
# List API users
sigfox api-users list
sigfox api-users list --limit 50 --offset 10
sigfox api-users list --profile-id 5138e7dfa2f1fffaf25fd409
sigfox api-users list --group-ids abc123,def456
sigfox api-users list --authorizations
sigfox api-users list --output json

# Get API user details
sigfox api-users get 5138e7dfa2f1fffaf25fd409
sigfox api-users get 5138e7dfa2f1fffaf25fd409 --authorizations
sigfox api-users get 5138e7dfa2f1fffaf25fd409 --output json

# Create a new API user
sigfox api-users create --group-id abc123 --name "My API User" \
    --timezone "Europe/Paris" --profile-ids prof1,prof2

# Update an API user
sigfox api-users update 5138e7dfa2f1fffaf25fd409 --name "New Name"
sigfox api-users update 5138e7dfa2f1fffaf25fd409 --timezone "America/New_York"
sigfox api-users update 5138e7dfa2f1fffaf25fd409 --profile-ids prof1,prof2,prof3

# Delete an API user (with confirmation prompt)
sigfox api-users delete 5138e7dfa2f1fffaf25fd409

# Delete an API user (skip confirmation)
sigfox api-users delete 5138e7dfa2f1fffaf25fd409 --force

# Associate profiles to an API user
sigfox api-users add-profiles 5138e7dfa2f1fffaf25fd409 --profile-ids prof1,prof2

# Remove a profile from an API user
sigfox api-users remove-profile 5138e7dfa2f1fffaf25fd409 51cc7155e4b00d18ddb99230

# Generate a new password for an API user
sigfox api-users renew-credential 5138e7dfa2f1fffaf25fd409
sigfox api-users renew-credential 5138e7dfa2f1fffaf25fd409 --force
```

### Operator Commands

```bash
# List operators
sigfox operators list
sigfox operators list --limit 50 --offset 10
sigfox operators list --group-ids abc123,def456 --deep
sigfox operators list --authorizations
sigfox operators list --output json

# Get operator details
sigfox operators get 5138e7dfa2f1fffaf25fd409
sigfox operators get 5138e7dfa2f1fffaf25fd409 --authorizations
sigfox operators get 5138e7dfa2f1fffaf25fd409 --output json
```

### User Commands

```bash
# List users
sigfox users list
sigfox users list --limit 50 --offset 10
sigfox users list --group-ids abc123,def456 --deep
sigfox users list --output json

# Get user details
sigfox users get 5138e7dfa2f1fffaf25fd409
sigfox users get 5138e7dfa2f1fffaf25fd409 --authorizations
sigfox users get 5138e7dfa2f1fffaf25fd409 --output json

# Create a new user
sigfox users create --group-id abc123 --first-name "John" --last-name "Doe" \
    --email "john.doe@example.com" --timezone "Europe/Paris" --role-ids role1,role2

# Update a user
sigfox users update 5138e7dfa2f1fffaf25fd409 --first-name "Jane"
sigfox users update 5138e7dfa2f1fffaf25fd409 --email "new@example.com" --timezone "America/New_York"

# Delete a user (with confirmation prompt)
sigfox users delete 5138e7dfa2f1fffaf25fd409

# Delete a user (skip confirmation)
sigfox users delete 5138e7dfa2f1fffaf25fd409 --force

# Associate roles to a user
sigfox users add-roles 5138e7dfa2f1fffaf25fd409 --role-ids role1,role2

# Remove a role from a user
sigfox users remove-role 5138e7dfa2f1fffaf25fd409 role001
sigfox users remove-role 5138e7dfa2f1fffaf25fd409 role001 --force
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

### List device types in table format

```bash
sigfox device-types list
```

Output:
```
                                    Device Types
┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓
┃ ID             ┃ Name         ┃ Description   ┃ Group   ┃ Contract   ┃ Keep Alive ┃ Creation Time       ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━┩
│ 5d8cdc8fea0... │ Type A       │ Sensors       │ Group A │ Contract 1 │ 3600       │ 2024-01-10 14:30:00 │
│ 5d8cdc8fea1... │ Type B       │ Trackers      │ Group B │ Contract 1 │ 7200       │ 2024-01-11 09:15:00 │
└────────────────┴──────────────┴───────────────┴─────────┴────────────┴────────────┴─────────────────────┘
```

### Create a new device type

```bash
sigfox device-types create --name "Production Sensors" --group-id abc123 --description "Temperature sensors"
```

Output:
```
✓ Device type created successfully (ID: 5d8cdc8fea06bb6e41234567)

                        Device Type Details
┌──────────────────┬─────────────────────────────────────┐
│ ID               │ 5d8cdc8fea06bb6e41234567            │
│ Name             │ Production Sensors                  │
│ Description      │ Temperature sensors                 │
│ Group            │ My Group                            │
│ Creation Time    │ 2024-01-15 10:30:45                 │
└──────────────────┴─────────────────────────────────────┘
```

### Get coverage prediction for a location

```bash
sigfox coverages global-prediction --lat 48.8566 --lng 2.3522
```

Output:
```
           Coverage Prediction
┌───────────────────────┬────────┐
│ Location Covered      │ ✓ Yes  │
│ Margin (redundancy 1) │ 10 dB  │
│ Margin (redundancy 2) │ 5 dB   │
│ Margin (redundancy 3) │ -2 dB  │
└───────────────────────┴────────┘
```

### Start a bulk coverage prediction job

```bash
sigfox coverages bulk-start --locations '[{"lat": 48.86, "lng": 2.35}, {"lat": 51.51, "lng": -0.13}]'
```

Output:
```
Bulk job started. Job ID: abc123xyz
Run: sigfox coverages bulk-get abc123xyz
```

### Get operator redundancy

```bash
sigfox coverages operator-redundancy --lat 48.8566 --lng 2.3522 --device-situation OUTDOOR
```

Output:
```
      Operator Redundancy
┌─────────────┬──────────────────┐
│ Redundancy  │ 3+ base stations │
└─────────────┴──────────────────┘
```

### List groups in table format

```bash
sigfox groups list
```

Output:
```
                                        Groups
┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓
┃ ID             ┃ Name         ┃ Type ┃ Timezone       ┃ Leaf ┃ Creation Time       ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━╇━━━━━━━━━━━━━━━━━━━━━┩
│ 572f120401...  │ Group A      │ 0    │ Europe/Paris   │ No   │ 2024-01-10 14:30:00 │
│ 572f120402...  │ Group B      │ 2    │ America/New... │ Yes  │ 2024-01-11 09:15:00 │
└────────────────┴──────────────┴──────┴────────────────┴──────┴─────────────────────┘
```

### Get group details

```bash
sigfox groups get 572f1204017975032d8ec1dd --output json
```

### Create a new group

```bash
sigfox groups create --name "Production" --description "Production sensors group" --type 8 --timezone "Europe/Paris" --parent-id 572f1204017975032d8ec1dd
```

Output:
```
✓ Group created successfully (ID: 572f1204017975032d8ec1ee)

                         Group Details
┌──────────────────┬─────────────────────────────────────┐
│ ID               │ 572f1204017975032d8ec1ee            │
│ Name             │ Production                          │
│ Description      │ Production sensors group            │
│ Type             │ 8                                   │
│ Timezone         │ Europe/Paris                        │
│ Creation Time    │ 2024-01-15 10:30:45                 │
└──────────────────┴─────────────────────────────────────┘
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
│       │   ├── api_users.py    # API user commands
│       │   ├── config_cmd.py   # Config commands
│       │   ├── coverages.py    # Coverage commands
│       │   ├── devices.py      # Device commands
│       │   ├── device_types.py # Device type commands
│       │   ├── groups.py       # Group commands
│       │   ├── operators.py    # Operator commands
│       │   └── users.py        # User commands
│       └── models/
│           ├── api_user.py     # API user models
│           ├── coverage.py     # Coverage models
│           ├── device.py       # Device models
│           ├── device_type.py  # Device type models
│           ├── group.py        # Group models
│           ├── message.py      # Message models
│           ├── operator.py     # Operator models
│           └── user.py         # User models
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

#### Devices
- `GET /devices/` - List devices
- `GET /devices/{id}` - Get device details
- `POST /devices/` - Create a device
- `PUT /devices/{id}` - Update a device
- `DELETE /devices/{id}` - Delete a device
- `GET /devices/{id}/messages` - List device messages

#### Device Types
- `GET /device-types/` - List device types
- `GET /device-types/{id}` - Get device type details
- `POST /device-types/` - Create a device type
- `PUT /device-types/{id}` - Update a device type
- `DELETE /device-types/{id}` - Delete a device type

#### Base Stations
- `GET /base-stations/{id}/messages` - Retrieve messages received by a base station

#### Coverages
- `GET /coverages/global/predictions` - Get coverage prediction for a single location
- `POST /coverages/global/predictions/bulk` - Start a bulk coverage prediction job
- `GET /coverages/global/predictions/bulk/{jobId}` - Get bulk prediction job results
- `GET /coverages/operators/redundancy` - Get operator redundancy coverage

#### Groups
- `GET /groups/` - List groups
- `GET /groups/{id}` - Get group details
- `POST /groups/` - Create a group
- `PUT /groups/{id}` - Update a group
- `DELETE /groups/{id}` - Delete a group
- `GET /groups/{id}/callbacks-not-delivered` - List undelivered callbacks
- `GET /groups/{id}/geoloc-payloads` - List geolocation payloads

#### API Users
- `GET /api-users/` - List API users
- `GET /api-users/{id}` - Get API user details
- `POST /api-users/` - Create an API user
- `PUT /api-users/{id}` - Update an API user
- `DELETE /api-users/{id}` - Delete an API user
- `PUT /api-users/{id}/profiles` - Associate profiles
- `DELETE /api-users/{id}/profiles/{profileId}` - Remove profile
- `PUT /api-users/{id}/renew-credential` - Generate new password

#### Operators
- `GET /operators/` - List operators
- `GET /operators/{id}` - Get operator details

#### Users
- `GET /users/` - List users
- `GET /users/{id}` - Get user details
- `POST /users/` - Create a user
- `PUT /users/{id}` - Update a user
- `DELETE /users/{id}` - Delete a user
- `PUT /users/{id}/roles` - Associate roles
- `DELETE /users/{id}/roles/{roleId}` - Remove role

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
