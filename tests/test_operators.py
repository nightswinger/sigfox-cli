"""Tests for operators commands."""

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


# --- List Operators ---


@respx.mock
def test_list_operators(runner):
    """Test listing operators."""
    respx.get("https://api.sigfox.com/v2/operators/").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [
                    {
                        "id": "op001",
                        "name": "Operator One",
                        "hostOperator": True,
                    },
                    {
                        "id": "op002",
                        "name": "Operator Two",
                        "hostOperator": False,
                    },
                ]
            },
        )
    )
    result = runner.invoke(cli, ["operators", "list"])
    assert result.exit_code == 0
    assert "Operator One" in result.output


@respx.mock
def test_list_operators_empty(runner):
    """Test listing operators when none exist."""
    respx.get("https://api.sigfox.com/v2/operators/").mock(
        return_value=httpx.Response(200, json={"data": []})
    )
    result = runner.invoke(cli, ["operators", "list"])
    assert result.exit_code == 0
    assert "No operators found" in result.output


@respx.mock
def test_list_operators_json(runner):
    """Test listing operators in JSON format."""
    respx.get("https://api.sigfox.com/v2/operators/").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [
                    {
                        "id": "op001",
                        "name": "Operator One",
                    }
                ]
            },
        )
    )
    result = runner.invoke(cli, ["operators", "list", "--output", "json"])
    assert result.exit_code == 0
    assert "op001" in result.output


@respx.mock
def test_list_operators_with_filters(runner):
    """Test listing operators with filters."""
    respx.get("https://api.sigfox.com/v2/operators/").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [
                    {
                        "id": "op001",
                        "name": "Operator One",
                    }
                ]
            },
        )
    )
    result = runner.invoke(
        cli,
        ["operators", "list", "--group-ids", "grp1,grp2", "--deep"],
    )
    assert result.exit_code == 0


# --- Get Operator ---


@respx.mock
def test_get_operator(runner):
    """Test getting operator details."""
    respx.get("https://api.sigfox.com/v2/operators/op001").mock(
        return_value=httpx.Response(
            200,
            json={
                "id": "op001",
                "name": "Operator One",
                "hostOperator": True,
                "contractId": "contract001",
            },
        )
    )
    result = runner.invoke(cli, ["operators", "get", "op001"])
    assert result.exit_code == 0
    assert "Operator One" in result.output


@respx.mock
def test_get_operator_json(runner):
    """Test getting operator details in JSON format."""
    respx.get("https://api.sigfox.com/v2/operators/op001").mock(
        return_value=httpx.Response(
            200,
            json={
                "id": "op001",
                "name": "Operator One",
            },
        )
    )
    result = runner.invoke(cli, ["operators", "get", "op001", "--output", "json"])
    assert result.exit_code == 0
    assert "op001" in result.output


@respx.mock
def test_get_operator_not_found(runner):
    """Test getting non-existent operator."""
    respx.get("https://api.sigfox.com/v2/operators/invalid").mock(
        return_value=httpx.Response(404, json={"message": "Not Found"})
    )
    result = runner.invoke(cli, ["operators", "get", "invalid"])
    assert result.exit_code != 0
