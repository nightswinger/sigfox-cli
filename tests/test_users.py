"""Tests for users commands."""

import httpx
import pytest
import respx
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


# --- List Users ---


@respx.mock
def test_list_users(runner):
    """Test listing users."""
    respx.get("https://api.sigfox.com/v2/users/").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [
                    {
                        "id": "usr001",
                        "firstName": "John",
                        "lastName": "Doe",
                        "email": "john@example.com",
                        "timezone": "Europe/Paris",
                    },
                    {
                        "id": "usr002",
                        "firstName": "Jane",
                        "lastName": "Smith",
                        "email": "jane@example.com",
                        "timezone": "America/New_York",
                    },
                ]
            },
        )
    )
    result = runner.invoke(cli, ["users", "list"])
    assert result.exit_code == 0
    assert "John" in result.output


@respx.mock
def test_list_users_empty(runner):
    """Test listing users when none exist."""
    respx.get("https://api.sigfox.com/v2/users/").mock(
        return_value=httpx.Response(200, json={"data": []})
    )
    result = runner.invoke(cli, ["users", "list"])
    assert result.exit_code == 0
    assert "No users found" in result.output


@respx.mock
def test_list_users_json(runner):
    """Test listing users in JSON format."""
    respx.get("https://api.sigfox.com/v2/users/").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [
                    {
                        "id": "usr001",
                        "firstName": "John",
                        "lastName": "Doe",
                    }
                ]
            },
        )
    )
    result = runner.invoke(cli, ["users", "list", "--output", "json"])
    assert result.exit_code == 0
    assert "usr001" in result.output


@respx.mock
def test_list_users_with_filters(runner):
    """Test listing users with filters."""
    respx.get("https://api.sigfox.com/v2/users/").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [
                    {
                        "id": "usr001",
                        "firstName": "John",
                        "lastName": "Doe",
                    }
                ]
            },
        )
    )
    result = runner.invoke(
        cli,
        ["users", "list", "--group-ids", "grp1,grp2", "--deep"],
    )
    assert result.exit_code == 0


# --- Get User ---


@respx.mock
def test_get_user(runner):
    """Test getting user details."""
    respx.get("https://api.sigfox.com/v2/users/usr001").mock(
        return_value=httpx.Response(
            200,
            json={
                "id": "usr001",
                "firstName": "John",
                "lastName": "Doe",
                "email": "john@example.com",
                "timezone": "Europe/Paris",
            },
        )
    )
    result = runner.invoke(cli, ["users", "get", "usr001"])
    assert result.exit_code == 0
    assert "John" in result.output


@respx.mock
def test_get_user_json(runner):
    """Test getting user details in JSON format."""
    respx.get("https://api.sigfox.com/v2/users/usr001").mock(
        return_value=httpx.Response(
            200,
            json={
                "id": "usr001",
                "firstName": "John",
                "lastName": "Doe",
            },
        )
    )
    result = runner.invoke(cli, ["users", "get", "usr001", "--output", "json"])
    assert result.exit_code == 0
    assert "usr001" in result.output


@respx.mock
def test_get_user_not_found(runner):
    """Test getting non-existent user."""
    respx.get("https://api.sigfox.com/v2/users/invalid").mock(
        return_value=httpx.Response(404, json={"message": "Not Found"})
    )
    result = runner.invoke(cli, ["users", "get", "invalid"])
    assert result.exit_code != 0


# --- Create User ---


@respx.mock
def test_create_user(runner):
    """Test creating a user."""
    respx.post("https://api.sigfox.com/v2/users/").mock(
        return_value=httpx.Response(201, json={"id": "newusr001"})
    )
    respx.get("https://api.sigfox.com/v2/users/newusr001").mock(
        return_value=httpx.Response(
            200,
            json={
                "id": "newusr001",
                "firstName": "John",
                "lastName": "Doe",
                "email": "john@example.com",
                "timezone": "Europe/Paris",
            },
        )
    )
    result = runner.invoke(
        cli,
        [
            "users",
            "create",
            "--group-id",
            "grp001",
            "--first-name",
            "John",
            "--last-name",
            "Doe",
            "--email",
            "john@example.com",
            "--timezone",
            "Europe/Paris",
            "--role-ids",
            "role001,role002",
        ],
    )
    assert result.exit_code == 0
    assert "created successfully" in result.output


def test_create_user_missing_email(runner):
    """Test creating a user without required email."""
    result = runner.invoke(
        cli,
        [
            "users",
            "create",
            "--group-id",
            "grp001",
            "--first-name",
            "John",
            "--last-name",
            "Doe",
            "--timezone",
            "Europe/Paris",
            "--role-ids",
            "role001",
        ],
    )
    assert result.exit_code != 0


def test_create_user_missing_role_ids(runner):
    """Test creating a user without required role-ids."""
    result = runner.invoke(
        cli,
        [
            "users",
            "create",
            "--group-id",
            "grp001",
            "--first-name",
            "John",
            "--last-name",
            "Doe",
            "--email",
            "john@example.com",
            "--timezone",
            "Europe/Paris",
        ],
    )
    assert result.exit_code != 0


# --- Update User ---


@respx.mock
def test_update_user(runner):
    """Test updating a user."""
    respx.put("https://api.sigfox.com/v2/users/usr001").mock(
        return_value=httpx.Response(204)
    )
    result = runner.invoke(
        cli,
        ["users", "update", "usr001", "--first-name", "Jane"],
    )
    assert result.exit_code == 0
    assert "updated successfully" in result.output


@respx.mock
def test_update_user_multiple_fields(runner):
    """Test updating a user with multiple fields."""
    respx.put("https://api.sigfox.com/v2/users/usr001").mock(
        return_value=httpx.Response(204)
    )
    result = runner.invoke(
        cli,
        [
            "users",
            "update",
            "usr001",
            "--first-name",
            "Jane",
            "--email",
            "jane@example.com",
            "--timezone",
            "America/New_York",
        ],
    )
    assert result.exit_code == 0
    assert "updated successfully" in result.output


def test_update_user_no_fields(runner):
    """Test updating a user with no fields specified."""
    result = runner.invoke(cli, ["users", "update", "usr001"])
    assert result.exit_code != 0
    assert "No update fields specified" in result.output


@respx.mock
def test_update_user_not_found(runner):
    """Test updating non-existent user."""
    respx.put("https://api.sigfox.com/v2/users/invalid").mock(
        return_value=httpx.Response(404, json={"message": "Not Found"})
    )
    result = runner.invoke(
        cli,
        ["users", "update", "invalid", "--first-name", "Test"],
    )
    assert result.exit_code != 0


# --- Delete User ---


@respx.mock
def test_delete_user_with_force(runner):
    """Test deleting a user with --force."""
    respx.delete("https://api.sigfox.com/v2/users/usr001").mock(
        return_value=httpx.Response(204)
    )
    result = runner.invoke(
        cli,
        ["users", "delete", "usr001", "--force"],
    )
    assert result.exit_code == 0
    assert "deleted successfully" in result.output


def test_delete_user_confirm_abort(runner):
    """Test deleting a user with confirmation denied."""
    result = runner.invoke(
        cli,
        ["users", "delete", "usr001"],
        input="n\n",
    )
    assert result.exit_code != 0


@respx.mock
def test_delete_user_confirm_accept(runner):
    """Test deleting a user with confirmation accepted."""
    respx.delete("https://api.sigfox.com/v2/users/usr001").mock(
        return_value=httpx.Response(204)
    )
    result = runner.invoke(
        cli,
        ["users", "delete", "usr001"],
        input="y\n",
    )
    assert result.exit_code == 0
    assert "deleted successfully" in result.output


@respx.mock
def test_delete_user_not_found(runner):
    """Test deleting non-existent user."""
    respx.delete("https://api.sigfox.com/v2/users/invalid").mock(
        return_value=httpx.Response(404, json={"message": "Not Found"})
    )
    result = runner.invoke(
        cli,
        ["users", "delete", "invalid", "--force"],
    )
    assert result.exit_code != 0


# --- Add Roles ---


@respx.mock
def test_add_roles(runner):
    """Test associating roles to a user."""
    respx.put("https://api.sigfox.com/v2/users/usr001/roles").mock(
        return_value=httpx.Response(204)
    )
    result = runner.invoke(
        cli,
        ["users", "add-roles", "usr001", "--role-ids", "role001,role002"],
    )
    assert result.exit_code == 0
    assert "Roles associated" in result.output


# --- Remove Role ---


@respx.mock
def test_remove_role_with_force(runner):
    """Test removing a role from a user with --force."""
    respx.delete("https://api.sigfox.com/v2/users/usr001/roles/role001").mock(
        return_value=httpx.Response(204)
    )
    result = runner.invoke(
        cli,
        ["users", "remove-role", "usr001", "role001", "--force"],
    )
    assert result.exit_code == 0
    assert "removed" in result.output


def test_remove_role_confirm_abort(runner):
    """Test removing a role with confirmation denied."""
    result = runner.invoke(
        cli,
        ["users", "remove-role", "usr001", "role001"],
        input="n\n",
    )
    assert result.exit_code != 0
