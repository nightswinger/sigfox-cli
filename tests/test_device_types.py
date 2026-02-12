"""Tests for device-types commands."""

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
def test_list_device_types(runner):
    """Test listing device types."""
    respx.get("https://api.sigfox.com/v2/device-types/").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [
                    {"id": "abc123", "name": "Type A", "description": "Test type"},
                    {"id": "def456", "name": "Type B", "description": None},
                ]
            },
        )
    )

    result = runner.invoke(cli, ["device-types", "list"])
    assert result.exit_code == 0
    assert "Type A" in result.output


@respx.mock
def test_list_device_types_empty(runner):
    """Test listing device types when none exist."""
    respx.get("https://api.sigfox.com/v2/device-types/").mock(
        return_value=httpx.Response(200, json={"data": []})
    )

    result = runner.invoke(cli, ["device-types", "list"])
    assert result.exit_code == 0
    assert "No device types found" in result.output


@respx.mock
def test_list_device_types_json(runner):
    """Test listing device types in JSON format."""
    respx.get("https://api.sigfox.com/v2/device-types/").mock(
        return_value=httpx.Response(
            200,
            json={"data": [{"id": "abc123", "name": "Type A"}]},
        )
    )

    result = runner.invoke(cli, ["device-types", "list", "--output", "json"])
    assert result.exit_code == 0
    assert "abc123" in result.output


@respx.mock
def test_list_device_types_with_filters(runner):
    """Test listing device types with filters."""
    respx.get("https://api.sigfox.com/v2/device-types/").mock(
        return_value=httpx.Response(
            200,
            json={"data": [{"id": "abc123", "name": "Type A"}]},
        )
    )

    result = runner.invoke(
        cli,
        ["device-types", "list", "--name", "Type", "--group-ids", "grp123", "--deep"],
    )
    assert result.exit_code == 0


@respx.mock
def test_get_device_type(runner):
    """Test getting device type details."""
    respx.get("https://api.sigfox.com/v2/device-types/abc123").mock(
        return_value=httpx.Response(
            200,
            json={"id": "abc123", "name": "Type A", "description": "Test"},
        )
    )

    result = runner.invoke(cli, ["device-types", "get", "abc123"])
    assert result.exit_code == 0
    assert "Type A" in result.output


@respx.mock
def test_get_device_type_json(runner):
    """Test getting device type details in JSON format."""
    respx.get("https://api.sigfox.com/v2/device-types/abc123").mock(
        return_value=httpx.Response(
            200,
            json={"id": "abc123", "name": "Type A"},
        )
    )

    result = runner.invoke(cli, ["device-types", "get", "abc123", "--output", "json"])
    assert result.exit_code == 0
    assert "abc123" in result.output


@respx.mock
def test_get_device_type_not_found(runner):
    """Test getting non-existent device type."""
    respx.get("https://api.sigfox.com/v2/device-types/invalid").mock(
        return_value=httpx.Response(404, json={"message": "Not Found"})
    )

    result = runner.invoke(cli, ["device-types", "get", "invalid"])
    assert result.exit_code != 0


@respx.mock
def test_create_device_type(runner):
    """Test creating a device type."""
    respx.post("https://api.sigfox.com/v2/device-types/").mock(
        return_value=httpx.Response(
            200,
            json={"id": "new123", "name": "New Type", "groupId": "grp123"},
        )
    )

    result = runner.invoke(
        cli,
        ["device-types", "create", "--name", "New Type", "--group-id", "grp123"],
    )
    assert result.exit_code == 0
    assert "created successfully" in result.output


@respx.mock
def test_create_device_type_with_options(runner):
    """Test creating a device type with optional fields."""
    respx.post("https://api.sigfox.com/v2/device-types/").mock(
        return_value=httpx.Response(
            200,
            json={
                "id": "new123",
                "name": "New Type",
                "groupId": "grp123",
                "description": "Test description",
            },
        )
    )

    result = runner.invoke(
        cli,
        [
            "device-types",
            "create",
            "--name",
            "New Type",
            "--group-id",
            "grp123",
            "--description",
            "Test description",
            "--keep-alive",
            "3600",
        ],
    )
    assert result.exit_code == 0
    assert "created successfully" in result.output


@respx.mock
def test_create_device_type_missing_name(runner):
    """Test creating a device type without required name."""
    result = runner.invoke(cli, ["device-types", "create", "--group-id", "grp123"])
    assert result.exit_code != 0


@respx.mock
def test_create_device_type_missing_group_id(runner):
    """Test creating a device type without required group-id."""
    result = runner.invoke(cli, ["device-types", "create", "--name", "Test"])
    assert result.exit_code != 0


@respx.mock
def test_update_device_type(runner):
    """Test updating a device type."""
    respx.put("https://api.sigfox.com/v2/device-types/abc123").mock(
        return_value=httpx.Response(204)
    )

    result = runner.invoke(
        cli,
        ["device-types", "update", "abc123", "--name", "Updated Name"],
    )
    assert result.exit_code == 0
    assert "updated successfully" in result.output


@respx.mock
def test_update_device_type_multiple_fields(runner):
    """Test updating a device type with multiple fields."""
    respx.put("https://api.sigfox.com/v2/device-types/abc123").mock(
        return_value=httpx.Response(204)
    )

    result = runner.invoke(
        cli,
        [
            "device-types",
            "update",
            "abc123",
            "--name",
            "Updated",
            "--description",
            "New description",
            "--keep-alive",
            "7200",
        ],
    )
    assert result.exit_code == 0
    assert "updated successfully" in result.output


def test_update_device_type_no_fields(runner):
    """Test updating a device type with no fields specified."""
    result = runner.invoke(cli, ["device-types", "update", "abc123"])
    assert result.exit_code != 0
    assert "No update fields specified" in result.output


@respx.mock
def test_update_device_type_not_found(runner):
    """Test updating non-existent device type."""
    respx.put("https://api.sigfox.com/v2/device-types/invalid").mock(
        return_value=httpx.Response(404, json={"message": "Not Found"})
    )

    result = runner.invoke(
        cli,
        ["device-types", "update", "invalid", "--name", "Test"],
    )
    assert result.exit_code != 0


@respx.mock
def test_delete_device_type_with_force(runner):
    """Test deleting a device type with --force."""
    respx.delete("https://api.sigfox.com/v2/device-types/abc123").mock(
        return_value=httpx.Response(204)
    )

    result = runner.invoke(
        cli,
        ["device-types", "delete", "abc123", "--force"],
    )
    assert result.exit_code == 0
    assert "deleted successfully" in result.output


def test_delete_device_type_confirm_abort(runner):
    """Test deleting a device type with confirmation denied."""
    result = runner.invoke(
        cli,
        ["device-types", "delete", "abc123"],
        input="n\n",
    )
    assert result.exit_code != 0


@respx.mock
def test_delete_device_type_confirm_accept(runner):
    """Test deleting a device type with confirmation accepted."""
    respx.delete("https://api.sigfox.com/v2/device-types/abc123").mock(
        return_value=httpx.Response(204)
    )

    result = runner.invoke(
        cli,
        ["device-types", "delete", "abc123"],
        input="y\n",
    )
    assert result.exit_code == 0
    assert "deleted successfully" in result.output


@respx.mock
def test_delete_device_type_not_found(runner):
    """Test deleting non-existent device type."""
    respx.delete("https://api.sigfox.com/v2/device-types/invalid").mock(
        return_value=httpx.Response(404, json={"message": "Not Found"})
    )

    result = runner.invoke(
        cli,
        ["device-types", "delete", "invalid", "--force"],
    )
    assert result.exit_code != 0
