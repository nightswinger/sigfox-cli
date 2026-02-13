"""Tests for groups commands."""

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


# --- List Groups ---

@respx.mock
def test_list_groups(runner):
    """Test listing groups."""
    respx.get("https://api.sigfox.com/v2/groups/").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [
                    {"id": "grp001", "name": "Group A", "type": 2},
                    {"id": "grp002", "name": "Group B", "type": 8},
                ]
            },
        )
    )

    result = runner.invoke(cli, ["groups", "list"])
    assert result.exit_code == 0
    assert "Group A" in result.output


@respx.mock
def test_list_groups_empty(runner):
    """Test listing groups when none exist."""
    respx.get("https://api.sigfox.com/v2/groups/").mock(
        return_value=httpx.Response(200, json={"data": []})
    )

    result = runner.invoke(cli, ["groups", "list"])
    assert result.exit_code == 0
    assert "No groups found" in result.output


@respx.mock
def test_list_groups_json(runner):
    """Test listing groups in JSON format."""
    respx.get("https://api.sigfox.com/v2/groups/").mock(
        return_value=httpx.Response(
            200,
            json={"data": [{"id": "grp001", "name": "Group A"}]},
        )
    )

    result = runner.invoke(cli, ["groups", "list", "--output", "json"])
    assert result.exit_code == 0
    assert "grp001" in result.output


@respx.mock
def test_list_groups_with_filters(runner):
    """Test listing groups with filters."""
    respx.get("https://api.sigfox.com/v2/groups/").mock(
        return_value=httpx.Response(
            200,
            json={"data": [{"id": "grp001", "name": "Group A"}]},
        )
    )

    result = runner.invoke(
        cli,
        ["groups", "list", "--parent-ids", "parent1,parent2", "--deep", "--name", "Group", "--types", "0,2"],
    )
    assert result.exit_code == 0


# --- Get Group ---

@respx.mock
def test_get_group(runner):
    """Test getting group details."""
    respx.get("https://api.sigfox.com/v2/groups/grp001").mock(
        return_value=httpx.Response(
            200,
            json={"id": "grp001", "name": "Group A", "type": 2, "timezone": "Europe/Paris"},
        )
    )

    result = runner.invoke(cli, ["groups", "get", "grp001"])
    assert result.exit_code == 0
    assert "Group A" in result.output


@respx.mock
def test_get_group_json(runner):
    """Test getting group details in JSON format."""
    respx.get("https://api.sigfox.com/v2/groups/grp001").mock(
        return_value=httpx.Response(
            200,
            json={"id": "grp001", "name": "Group A"},
        )
    )

    result = runner.invoke(cli, ["groups", "get", "grp001", "--output", "json"])
    assert result.exit_code == 0
    assert "grp001" in result.output


@respx.mock
def test_get_group_not_found(runner):
    """Test getting non-existent group."""
    respx.get("https://api.sigfox.com/v2/groups/invalid").mock(
        return_value=httpx.Response(404, json={"message": "Not Found"})
    )

    result = runner.invoke(cli, ["groups", "get", "invalid"])
    assert result.exit_code != 0


# --- Create Group ---

@respx.mock
def test_create_group(runner):
    """Test creating a group."""
    respx.post("https://api.sigfox.com/v2/groups/").mock(
        return_value=httpx.Response(201, json={"id": "newgrp123"})
    )
    respx.get("https://api.sigfox.com/v2/groups/newgrp123").mock(
        return_value=httpx.Response(
            200,
            json={"id": "newgrp123", "name": "New Group", "type": 8, "timezone": "Europe/Paris"},
        )
    )

    result = runner.invoke(
        cli,
        [
            "groups", "create",
            "--name", "New Group",
            "--description", "Test description",
            "--type", "8",
            "--timezone", "Europe/Paris",
            "--parent-id", "parentgrp001",
        ],
    )
    assert result.exit_code == 0
    assert "created successfully" in result.output


def test_create_group_missing_name(runner):
    """Test creating a group without required name."""
    result = runner.invoke(
        cli,
        [
            "groups", "create",
            "--description", "Test",
            "--type", "8",
            "--timezone", "Europe/Paris",
            "--parent-id", "parentgrp001",
        ],
    )
    assert result.exit_code != 0


def test_create_group_missing_parent_id(runner):
    """Test creating a group without required parent-id."""
    result = runner.invoke(
        cli,
        [
            "groups", "create",
            "--name", "Test",
            "--description", "Test",
            "--type", "8",
            "--timezone", "Europe/Paris",
        ],
    )
    assert result.exit_code != 0


# --- Update Group ---

@respx.mock
def test_update_group(runner):
    """Test updating a group."""
    respx.put("https://api.sigfox.com/v2/groups/grp001").mock(
        return_value=httpx.Response(204)
    )

    result = runner.invoke(
        cli,
        ["groups", "update", "grp001", "--name", "Updated Name"],
    )
    assert result.exit_code == 0
    assert "updated successfully" in result.output


@respx.mock
def test_update_group_multiple_fields(runner):
    """Test updating a group with multiple fields."""
    respx.put("https://api.sigfox.com/v2/groups/grp001").mock(
        return_value=httpx.Response(204)
    )

    result = runner.invoke(
        cli,
        [
            "groups", "update", "grp001",
            "--name", "Updated",
            "--description", "New description",
            "--timezone", "America/New_York",
        ],
    )
    assert result.exit_code == 0
    assert "updated successfully" in result.output


def test_update_group_no_fields(runner):
    """Test updating a group with no fields specified."""
    result = runner.invoke(cli, ["groups", "update", "grp001"])
    assert result.exit_code != 0
    assert "No update fields specified" in result.output


@respx.mock
def test_update_group_not_found(runner):
    """Test updating non-existent group."""
    respx.put("https://api.sigfox.com/v2/groups/invalid").mock(
        return_value=httpx.Response(404, json={"message": "Not Found"})
    )

    result = runner.invoke(
        cli,
        ["groups", "update", "invalid", "--name", "Test"],
    )
    assert result.exit_code != 0


# --- Delete Group ---

@respx.mock
def test_delete_group_with_force(runner):
    """Test deleting a group with --force."""
    respx.delete("https://api.sigfox.com/v2/groups/grp001").mock(
        return_value=httpx.Response(204)
    )

    result = runner.invoke(
        cli,
        ["groups", "delete", "grp001", "--force"],
    )
    assert result.exit_code == 0
    assert "deleted successfully" in result.output


def test_delete_group_confirm_abort(runner):
    """Test deleting a group with confirmation denied."""
    result = runner.invoke(
        cli,
        ["groups", "delete", "grp001"],
        input="n\n",
    )
    assert result.exit_code != 0


@respx.mock
def test_delete_group_confirm_accept(runner):
    """Test deleting a group with confirmation accepted."""
    respx.delete("https://api.sigfox.com/v2/groups/grp001").mock(
        return_value=httpx.Response(204)
    )

    result = runner.invoke(
        cli,
        ["groups", "delete", "grp001"],
        input="y\n",
    )
    assert result.exit_code == 0
    assert "deleted successfully" in result.output


@respx.mock
def test_delete_group_not_found(runner):
    """Test deleting non-existent group."""
    respx.delete("https://api.sigfox.com/v2/groups/invalid").mock(
        return_value=httpx.Response(404, json={"message": "Not Found"})
    )

    result = runner.invoke(
        cli,
        ["groups", "delete", "invalid", "--force"],
    )
    assert result.exit_code != 0


# --- Callbacks Not Delivered ---

@respx.mock
def test_callbacks_not_delivered(runner):
    """Test listing undelivered callbacks for a group."""
    respx.get("https://api.sigfox.com/v2/groups/grp001/callbacks-not-delivered").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [
                    {"device": "1A2B3C", "time": 1609459200000, "status": "error", "message": "Timeout"},
                    {"device": "4D5E6F", "time": 1609459100000, "status": "error", "message": "Connection refused"},
                ]
            },
        )
    )

    result = runner.invoke(cli, ["groups", "callbacks-not-delivered", "grp001"])
    assert result.exit_code == 0


@respx.mock
def test_callbacks_not_delivered_empty(runner):
    """Test listing callbacks when none exist."""
    respx.get("https://api.sigfox.com/v2/groups/grp001/callbacks-not-delivered").mock(
        return_value=httpx.Response(200, json={"data": []})
    )

    result = runner.invoke(cli, ["groups", "callbacks-not-delivered", "grp001"])
    assert result.exit_code == 0
    assert "No undelivered callbacks found" in result.output


# --- Geoloc Payloads ---

@respx.mock
def test_geoloc_payloads(runner):
    """Test listing geolocation payloads for a group."""
    respx.get("https://api.sigfox.com/v2/groups/grp001/geoloc-payloads").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [
                    {"id": "geo001", "name": "Payload A"},
                    {"id": "geo002", "name": "Payload B"},
                ]
            },
        )
    )

    result = runner.invoke(cli, ["groups", "geoloc-payloads", "grp001"])
    assert result.exit_code == 0


@respx.mock
def test_geoloc_payloads_empty(runner):
    """Test listing geolocation payloads when none exist."""
    respx.get("https://api.sigfox.com/v2/groups/grp001/geoloc-payloads").mock(
        return_value=httpx.Response(200, json={"data": []})
    )

    result = runner.invoke(cli, ["groups", "geoloc-payloads", "grp001"])
    assert result.exit_code == 0
    assert "No geolocation payloads found" in result.output
