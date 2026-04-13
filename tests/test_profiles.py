"""Tests for profiles commands."""

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


# --- List Profiles ---


@respx.mock
def test_list_profiles(runner):
    """Test listing profiles."""
    respx.get("https://api.sigfox.com/v2/profiles/").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [
                    {
                        "id": "prof001",
                        "name": "CUSTOMER [R]",
                    },
                    {
                        "id": "prof002",
                        "name": "CUSTOMER [RW]",
                    },
                ]
            },
        )
    )
    result = runner.invoke(cli, ["profiles", "list", "--group-id", "grp001"])
    assert result.exit_code == 0
    assert "CUSTOMER [R]" in result.output


@respx.mock
def test_list_profiles_empty(runner):
    """Test listing profiles when none exist."""
    respx.get("https://api.sigfox.com/v2/profiles/").mock(
        return_value=httpx.Response(200, json={"data": []})
    )
    result = runner.invoke(cli, ["profiles", "list", "--group-id", "grp001"])
    assert result.exit_code == 0
    assert "No profiles found" in result.output


@respx.mock
def test_list_profiles_json(runner):
    """Test listing profiles in JSON format."""
    respx.get("https://api.sigfox.com/v2/profiles/").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [
                    {
                        "id": "prof001",
                        "name": "CUSTOMER [R]",
                    }
                ]
            },
        )
    )
    result = runner.invoke(
        cli, ["profiles", "list", "--group-id", "grp001", "--output", "json"]
    )
    assert result.exit_code == 0
    assert "prof001" in result.output


@respx.mock
def test_list_profiles_with_inherit(runner):
    """Test listing profiles with --inherit flag."""
    respx.get("https://api.sigfox.com/v2/profiles/").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [
                    {
                        "id": "prof001",
                        "name": "CUSTOMER [R]",
                    }
                ]
            },
        )
    )
    result = runner.invoke(
        cli, ["profiles", "list", "--group-id", "grp001", "--inherit"]
    )
    assert result.exit_code == 0


# --- Get Profile ---


@respx.mock
def test_get_profile(runner):
    """Test getting profile details."""
    respx.get("https://api.sigfox.com/v2/profiles/prof001").mock(
        return_value=httpx.Response(
            200,
            json={
                "id": "prof001",
                "name": "CUSTOMER [R]",
                "group": {"id": "grp001", "name": "My Group"},
            },
        )
    )
    result = runner.invoke(cli, ["profiles", "get", "prof001"])
    assert result.exit_code == 0
    assert "CUSTOMER [R]" in result.output


@respx.mock
def test_get_profile_json(runner):
    """Test getting profile details in JSON format."""
    respx.get("https://api.sigfox.com/v2/profiles/prof001").mock(
        return_value=httpx.Response(
            200,
            json={
                "id": "prof001",
                "name": "CUSTOMER [R]",
            },
        )
    )
    result = runner.invoke(cli, ["profiles", "get", "prof001", "--output", "json"])
    assert result.exit_code == 0
    assert "prof001" in result.output


@respx.mock
def test_get_profile_not_found(runner):
    """Test getting non-existent profile."""
    respx.get("https://api.sigfox.com/v2/profiles/invalid").mock(
        return_value=httpx.Response(404, json={"message": "Not Found"})
    )
    result = runner.invoke(cli, ["profiles", "get", "invalid"])
    assert result.exit_code != 0


def test_list_profiles_missing_group_id(runner):
    """Test listing profiles without required --group-id fails."""
    result = runner.invoke(cli, ["profiles", "list"])
    assert result.exit_code != 0
    assert "group-id" in result.output.lower() or "missing" in result.output.lower()
