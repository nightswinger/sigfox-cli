"""Tests for devices commands."""

import pytest
import respx
import httpx
from click.testing import CliRunner

from sigfox_cli.app import cli


@pytest.fixture
def runner():
    """Create a CLI test runner."""
    return CliRunner()


@pytest.fixture(autouse=True)
def mock_config(monkeypatch):
    """Mock configuration to avoid reading real config files."""
    monkeypatch.setenv("SIGFOX_API_LOGIN", "test_login")
    monkeypatch.setenv("SIGFOX_API_PASSWORD", "test_password")


@respx.mock
def test_list_devices(runner):
    """Test listing devices."""
    respx.get("https://api.sigfox.com/v2/devices/").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [
                    {"id": "1A2B3C", "name": "Device A", "deviceType": {"id": "abc123"}},
                    {"id": "4D5E6F", "name": "Device B", "deviceType": {"id": "def456"}},
                ]
            },
        )
    )

    result = runner.invoke(cli, ["devices", "list"])
    assert result.exit_code == 0
    assert "Device A" in result.output


@respx.mock
def test_list_devices_empty(runner):
    """Test listing devices when none exist."""
    respx.get("https://api.sigfox.com/v2/devices/").mock(
        return_value=httpx.Response(200, json={"data": []})
    )

    result = runner.invoke(cli, ["devices", "list"])
    assert result.exit_code == 0
    assert "No devices found" in result.output


@respx.mock
def test_get_device(runner):
    """Test getting device details."""
    respx.get("https://api.sigfox.com/v2/devices/1A2B3C").mock(
        return_value=httpx.Response(
            200,
            json={"id": "1A2B3C", "name": "Device A", "deviceType": {"id": "abc123"}},
        )
    )

    result = runner.invoke(cli, ["devices", "get", "1A2B3C"])
    assert result.exit_code == 0
    assert "Device A" in result.output


@respx.mock
def test_get_device_not_found(runner):
    """Test getting non-existent device."""
    respx.get("https://api.sigfox.com/v2/devices/invalid").mock(
        return_value=httpx.Response(404, json={"message": "Not Found"})
    )

    result = runner.invoke(cli, ["devices", "get", "invalid"])
    assert result.exit_code != 0


@respx.mock
def test_create_device(runner):
    """Test creating a device."""
    respx.post("https://api.sigfox.com/v2/devices/").mock(
        return_value=httpx.Response(201, json={"id": "1A2B3C"})
    )
    respx.get("https://api.sigfox.com/v2/devices/1A2B3C").mock(
        return_value=httpx.Response(
            200,
            json={
                "id": "1A2B3C",
                "name": "New Device",
                "deviceType": {"id": "abc123"},
            },
        )
    )

    result = runner.invoke(
        cli,
        [
            "devices",
            "create",
            "--device-id",
            "1A2B3C",
            "--name",
            "New Device",
            "--device-type-id",
            "abc123",
            "--pac",
            "ABC123DEF456",
        ],
    )
    assert result.exit_code == 0
    assert "created successfully" in result.output


@respx.mock
def test_create_device_with_location(runner):
    """Test creating a device with location."""
    respx.post("https://api.sigfox.com/v2/devices/").mock(
        return_value=httpx.Response(201, json={"id": "1A2B3C"})
    )
    respx.get("https://api.sigfox.com/v2/devices/1A2B3C").mock(
        return_value=httpx.Response(
            200,
            json={
                "id": "1A2B3C",
                "name": "Located Device",
                "lat": 48.8585715,
                "lng": 2.2922923,
            },
        )
    )

    result = runner.invoke(
        cli,
        [
            "devices",
            "create",
            "--device-id",
            "1A2B3C",
            "--name",
            "Located Device",
            "--device-type-id",
            "abc123",
            "--pac",
            "ABC123",
            "--lat",
            "48.8585715",
            "--lng",
            "2.2922923",
        ],
    )
    assert result.exit_code == 0
    assert "created successfully" in result.output


@respx.mock
def test_create_device_prototype(runner):
    """Test creating a prototype device."""
    respx.post("https://api.sigfox.com/v2/devices/").mock(
        return_value=httpx.Response(201, json={"id": "1A2B3C"})
    )
    respx.get("https://api.sigfox.com/v2/devices/1A2B3C").mock(
        return_value=httpx.Response(
            200,
            json={
                "id": "1A2B3C",
                "name": "Prototype",
                "prototype": True,
            },
        )
    )

    result = runner.invoke(
        cli,
        [
            "devices",
            "create",
            "--device-id",
            "1A2B3C",
            "--name",
            "Prototype",
            "--device-type-id",
            "abc123",
            "--pac",
            "ABC123",
            "--prototype",
        ],
    )
    assert result.exit_code == 0
    assert "created successfully" in result.output


def test_create_device_missing_required_fields(runner):
    """Test creating a device without required fields."""
    result = runner.invoke(
        cli,
        ["devices", "create", "--name", "Test"],
    )
    assert result.exit_code != 0


@respx.mock
def test_update_device(runner):
    """Test updating a device."""
    respx.put("https://api.sigfox.com/v2/devices/1A2B3C").mock(
        return_value=httpx.Response(204)
    )

    result = runner.invoke(
        cli,
        ["devices", "update", "1A2B3C", "--name", "Updated Name"],
    )
    assert result.exit_code == 0
    assert "updated successfully" in result.output


@respx.mock
def test_update_device_multiple_fields(runner):
    """Test updating a device with multiple fields."""
    respx.put("https://api.sigfox.com/v2/devices/1A2B3C").mock(
        return_value=httpx.Response(204)
    )

    result = runner.invoke(
        cli,
        [
            "devices",
            "update",
            "1A2B3C",
            "--name",
            "Updated",
            "--lat",
            "48.8585715",
            "--lng",
            "2.2922923",
        ],
    )
    assert result.exit_code == 0
    assert "updated successfully" in result.output


def test_update_device_no_fields(runner):
    """Test updating a device with no fields specified."""
    result = runner.invoke(cli, ["devices", "update", "1A2B3C"])
    assert result.exit_code != 0
    assert "No update fields specified" in result.output


@respx.mock
def test_update_device_not_found(runner):
    """Test updating non-existent device."""
    respx.put("https://api.sigfox.com/v2/devices/invalid").mock(
        return_value=httpx.Response(404, json={"message": "Not Found"})
    )

    result = runner.invoke(
        cli,
        ["devices", "update", "invalid", "--name", "Test"],
    )
    assert result.exit_code != 0


@respx.mock
def test_delete_device_with_force(runner):
    """Test deleting a device with --force."""
    respx.delete("https://api.sigfox.com/v2/devices/1A2B3C").mock(
        return_value=httpx.Response(204)
    )

    result = runner.invoke(
        cli,
        ["devices", "delete", "1A2B3C", "--force"],
    )
    assert result.exit_code == 0
    assert "deleted successfully" in result.output


def test_delete_device_confirm_abort(runner):
    """Test deleting a device with confirmation denied."""
    result = runner.invoke(
        cli,
        ["devices", "delete", "1A2B3C"],
        input="n\n",
    )
    assert result.exit_code != 0


@respx.mock
def test_delete_device_confirm_accept(runner):
    """Test deleting a device with confirmation accepted."""
    respx.delete("https://api.sigfox.com/v2/devices/1A2B3C").mock(
        return_value=httpx.Response(204)
    )

    result = runner.invoke(
        cli,
        ["devices", "delete", "1A2B3C"],
        input="y\n",
    )
    assert result.exit_code == 0
    assert "deleted successfully" in result.output


@respx.mock
def test_delete_device_not_found(runner):
    """Test deleting non-existent device."""
    respx.delete("https://api.sigfox.com/v2/devices/invalid").mock(
        return_value=httpx.Response(404, json={"message": "Not Found"})
    )

    result = runner.invoke(
        cli,
        ["devices", "delete", "invalid", "--force"],
    )
    assert result.exit_code != 0


@respx.mock
def test_list_messages(runner):
    """Test listing messages for a device."""
    respx.get("https://api.sigfox.com/v2/devices/1A2B3C/messages").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [
                    {"time": 1609459200000, "data": "abcd1234"},
                    {"time": 1609459100000, "data": "efgh5678"},
                ]
            },
        )
    )

    result = runner.invoke(cli, ["devices", "messages", "1A2B3C"])
    assert result.exit_code == 0


@respx.mock
def test_list_messages_empty(runner):
    """Test listing messages when none exist."""
    respx.get("https://api.sigfox.com/v2/devices/1A2B3C/messages").mock(
        return_value=httpx.Response(200, json={"data": []})
    )

    result = runner.invoke(cli, ["devices", "messages", "1A2B3C"])
    assert result.exit_code == 0
    assert "No messages found" in result.output
