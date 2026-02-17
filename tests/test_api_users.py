"""Tests for api-users commands."""

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


# --- List API Users ---


@respx.mock
def test_list_api_users(runner):
    """Test listing API users."""
    respx.get("https://api.sigfox.com/v2/api-users/").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [
                    {"id": "usr001", "name": "User A", "timezone": "Europe/Paris"},
                    {"id": "usr002", "name": "User B", "timezone": "America/New_York"},
                ]
            },
        )
    )
    result = runner.invoke(cli, ["api-users", "list"])
    assert result.exit_code == 0
    assert "User A" in result.output


@respx.mock
def test_list_api_users_empty(runner):
    """Test listing API users when none exist."""
    respx.get("https://api.sigfox.com/v2/api-users/").mock(
        return_value=httpx.Response(200, json={"data": []})
    )
    result = runner.invoke(cli, ["api-users", "list"])
    assert result.exit_code == 0
    assert "No API users found" in result.output


@respx.mock
def test_list_api_users_json(runner):
    """Test listing API users in JSON format."""
    respx.get("https://api.sigfox.com/v2/api-users/").mock(
        return_value=httpx.Response(
            200,
            json={"data": [{"id": "usr001", "name": "User A"}]},
        )
    )
    result = runner.invoke(cli, ["api-users", "list", "--output", "json"])
    assert result.exit_code == 0
    assert "usr001" in result.output


@respx.mock
def test_list_api_users_with_filters(runner):
    """Test listing API users with filters."""
    respx.get("https://api.sigfox.com/v2/api-users/").mock(
        return_value=httpx.Response(
            200,
            json={"data": [{"id": "usr001", "name": "User A"}]},
        )
    )
    result = runner.invoke(
        cli,
        ["api-users", "list", "--profile-id", "prof001", "--group-ids", "grp1,grp2"],
    )
    assert result.exit_code == 0


# --- Get API User ---


@respx.mock
def test_get_api_user(runner):
    """Test getting API user details."""
    respx.get("https://api.sigfox.com/v2/api-users/usr001").mock(
        return_value=httpx.Response(
            200,
            json={"id": "usr001", "name": "User A", "timezone": "Europe/Paris"},
        )
    )
    result = runner.invoke(cli, ["api-users", "get", "usr001"])
    assert result.exit_code == 0
    assert "User A" in result.output


@respx.mock
def test_get_api_user_json(runner):
    """Test getting API user details in JSON format."""
    respx.get("https://api.sigfox.com/v2/api-users/usr001").mock(
        return_value=httpx.Response(
            200,
            json={"id": "usr001", "name": "User A"},
        )
    )
    result = runner.invoke(cli, ["api-users", "get", "usr001", "--output", "json"])
    assert result.exit_code == 0
    assert "usr001" in result.output


@respx.mock
def test_get_api_user_not_found(runner):
    """Test getting non-existent API user."""
    respx.get("https://api.sigfox.com/v2/api-users/invalid").mock(
        return_value=httpx.Response(404, json={"message": "Not Found"})
    )
    result = runner.invoke(cli, ["api-users", "get", "invalid"])
    assert result.exit_code != 0


# --- Create API User ---


@respx.mock
def test_create_api_user(runner):
    """Test creating an API user."""
    respx.post("https://api.sigfox.com/v2/api-users/").mock(
        return_value=httpx.Response(201, json={"id": "newusr001"})
    )
    respx.get("https://api.sigfox.com/v2/api-users/newusr001").mock(
        return_value=httpx.Response(
            200,
            json={"id": "newusr001", "name": "New User", "timezone": "Europe/Paris"},
        )
    )
    result = runner.invoke(
        cli,
        [
            "api-users",
            "create",
            "--group-id",
            "grp001",
            "--name",
            "New User",
            "--timezone",
            "Europe/Paris",
            "--profile-ids",
            "prof001,prof002",
        ],
    )
    assert result.exit_code == 0
    assert "created successfully" in result.output


def test_create_api_user_missing_name(runner):
    """Test creating an API user without required name."""
    result = runner.invoke(
        cli,
        [
            "api-users",
            "create",
            "--group-id",
            "grp001",
            "--timezone",
            "Europe/Paris",
            "--profile-ids",
            "prof001",
        ],
    )
    assert result.exit_code != 0


def test_create_api_user_missing_profile_ids(runner):
    """Test creating an API user without required profile-ids."""
    result = runner.invoke(
        cli,
        [
            "api-users",
            "create",
            "--group-id",
            "grp001",
            "--name",
            "Test",
            "--timezone",
            "Europe/Paris",
        ],
    )
    assert result.exit_code != 0


# --- Update API User ---


@respx.mock
def test_update_api_user(runner):
    """Test updating an API user."""
    respx.put("https://api.sigfox.com/v2/api-users/usr001").mock(
        return_value=httpx.Response(204)
    )
    result = runner.invoke(
        cli,
        ["api-users", "update", "usr001", "--name", "Updated Name"],
    )
    assert result.exit_code == 0
    assert "updated successfully" in result.output


@respx.mock
def test_update_api_user_multiple_fields(runner):
    """Test updating an API user with multiple fields."""
    respx.put("https://api.sigfox.com/v2/api-users/usr001").mock(
        return_value=httpx.Response(204)
    )
    result = runner.invoke(
        cli,
        [
            "api-users",
            "update",
            "usr001",
            "--name",
            "Updated",
            "--timezone",
            "America/New_York",
        ],
    )
    assert result.exit_code == 0
    assert "updated successfully" in result.output


def test_update_api_user_no_fields(runner):
    """Test updating an API user with no fields specified."""
    result = runner.invoke(cli, ["api-users", "update", "usr001"])
    assert result.exit_code != 0
    assert "No update fields specified" in result.output


@respx.mock
def test_update_api_user_not_found(runner):
    """Test updating non-existent API user."""
    respx.put("https://api.sigfox.com/v2/api-users/invalid").mock(
        return_value=httpx.Response(404, json={"message": "Not Found"})
    )
    result = runner.invoke(
        cli,
        ["api-users", "update", "invalid", "--name", "Test"],
    )
    assert result.exit_code != 0


# --- Delete API User ---


@respx.mock
def test_delete_api_user_with_force(runner):
    """Test deleting an API user with --force."""
    respx.delete("https://api.sigfox.com/v2/api-users/usr001").mock(
        return_value=httpx.Response(204)
    )
    result = runner.invoke(
        cli,
        ["api-users", "delete", "usr001", "--force"],
    )
    assert result.exit_code == 0
    assert "deleted successfully" in result.output


def test_delete_api_user_confirm_abort(runner):
    """Test deleting an API user with confirmation denied."""
    result = runner.invoke(
        cli,
        ["api-users", "delete", "usr001"],
        input="n\n",
    )
    assert result.exit_code != 0


@respx.mock
def test_delete_api_user_confirm_accept(runner):
    """Test deleting an API user with confirmation accepted."""
    respx.delete("https://api.sigfox.com/v2/api-users/usr001").mock(
        return_value=httpx.Response(204)
    )
    result = runner.invoke(
        cli,
        ["api-users", "delete", "usr001"],
        input="y\n",
    )
    assert result.exit_code == 0
    assert "deleted successfully" in result.output


@respx.mock
def test_delete_api_user_not_found(runner):
    """Test deleting non-existent API user."""
    respx.delete("https://api.sigfox.com/v2/api-users/invalid").mock(
        return_value=httpx.Response(404, json={"message": "Not Found"})
    )
    result = runner.invoke(
        cli,
        ["api-users", "delete", "invalid", "--force"],
    )
    assert result.exit_code != 0


# --- Add Profiles ---


@respx.mock
def test_add_profiles(runner):
    """Test associating profiles to an API user."""
    respx.put("https://api.sigfox.com/v2/api-users/usr001/profiles").mock(
        return_value=httpx.Response(204)
    )
    result = runner.invoke(
        cli,
        ["api-users", "add-profiles", "usr001", "--profile-ids", "prof001,prof002"],
    )
    assert result.exit_code == 0
    assert "Profiles associated" in result.output


# --- Remove Profile ---


@respx.mock
def test_remove_profile_with_force(runner):
    """Test removing a profile from an API user with --force."""
    respx.delete("https://api.sigfox.com/v2/api-users/usr001/profiles/prof001").mock(
        return_value=httpx.Response(204)
    )
    result = runner.invoke(
        cli,
        ["api-users", "remove-profile", "usr001", "prof001", "--force"],
    )
    assert result.exit_code == 0
    assert "removed" in result.output


def test_remove_profile_confirm_abort(runner):
    """Test removing a profile with confirmation denied."""
    result = runner.invoke(
        cli,
        ["api-users", "remove-profile", "usr001", "prof001"],
        input="n\n",
    )
    assert result.exit_code != 0


# --- Renew Credential ---


@respx.mock
def test_renew_credential_with_force(runner):
    """Test renewing credential with --force."""
    respx.put("https://api.sigfox.com/v2/api-users/usr001/renew-credential").mock(
        return_value=httpx.Response(
            200,
            json={"accessToken": "new_secret_token_xyz"},
        )
    )
    result = runner.invoke(
        cli,
        ["api-users", "renew-credential", "usr001", "--force"],
    )
    assert result.exit_code == 0
    assert "new_secret_token_xyz" in result.output


def test_renew_credential_confirm_abort(runner):
    """Test renewing credential with confirmation denied."""
    result = runner.invoke(
        cli,
        ["api-users", "renew-credential", "usr001"],
        input="n\n",
    )
    assert result.exit_code != 0


@respx.mock
def test_renew_credential_json(runner):
    """Test renewing credential with JSON output."""
    respx.put("https://api.sigfox.com/v2/api-users/usr001/renew-credential").mock(
        return_value=httpx.Response(
            200,
            json={"accessToken": "new_secret_token_xyz"},
        )
    )
    result = runner.invoke(
        cli,
        ["api-users", "renew-credential", "usr001", "--force", "--output", "json"],
    )
    assert result.exit_code == 0
    assert "accessToken" in result.output
