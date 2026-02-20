"""Tests for contract-infos commands."""

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


# --- List Contract Infos ---


@respx.mock
def test_list_contract_infos(runner):
    """Test listing contract infos."""
    respx.get("https://api.sigfox.com/v2/contract-infos/").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [
                    {
                        "id": "ci001",
                        "name": "My Contract",
                        "contractId": "BSS-001",
                        "subscriptionPlan": 1,
                        "tokensInUse": 10,
                        "maxTokens": 100,
                    },
                    {
                        "id": "ci002",
                        "name": "Dev Contract",
                        "contractId": "BSS-002",
                        "subscriptionPlan": 5,
                        "tokensInUse": 3,
                        "maxTokens": 50,
                    },
                ]
            },
        )
    )
    result = runner.invoke(cli, ["contract-infos", "list"])
    assert result.exit_code == 0
    assert "ci001" in result.output


@respx.mock
def test_list_contract_infos_empty(runner):
    """Test listing contract infos when none exist."""
    respx.get("https://api.sigfox.com/v2/contract-infos/").mock(
        return_value=httpx.Response(200, json={"data": []})
    )
    result = runner.invoke(cli, ["contract-infos", "list"])
    assert result.exit_code == 0
    assert "No contract infos found" in result.output


@respx.mock
def test_list_contract_infos_json(runner):
    """Test listing contract infos in JSON format."""
    respx.get("https://api.sigfox.com/v2/contract-infos/").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [
                    {
                        "id": "ci001",
                        "name": "My Contract",
                    }
                ]
            },
        )
    )
    result = runner.invoke(cli, ["contract-infos", "list", "--output", "json"])
    assert result.exit_code == 0
    assert "ci001" in result.output


@respx.mock
def test_list_contract_infos_with_filters(runner):
    """Test listing contract infos with filters."""
    respx.get("https://api.sigfox.com/v2/contract-infos/").mock(
        return_value=httpx.Response(
            200,
            json={"data": [{"id": "ci001", "name": "My Contract"}]},
        )
    )
    result = runner.invoke(
        cli,
        ["contract-infos", "list", "--group-id", "grp001", "--subscription-plan", "1"],
    )
    assert result.exit_code == 0


# --- Get Contract Info ---


@respx.mock
def test_get_contract_info(runner):
    """Test getting contract info details."""
    respx.get("https://api.sigfox.com/v2/contract-infos/ci001").mock(
        return_value=httpx.Response(
            200,
            json={
                "id": "ci001",
                "name": "My Contract",
                "contractId": "BSS-001",
                "pricingModel": 2,
                "subscriptionPlan": 1,
                "timezone": "Europe/Paris",
                "group": {"id": "grp001", "name": "My Group"},
            },
        )
    )
    result = runner.invoke(cli, ["contract-infos", "get", "ci001"])
    assert result.exit_code == 0
    assert "My Contract" in result.output


@respx.mock
def test_get_contract_info_json(runner):
    """Test getting contract info details in JSON format."""
    respx.get("https://api.sigfox.com/v2/contract-infos/ci001").mock(
        return_value=httpx.Response(
            200,
            json={
                "id": "ci001",
                "name": "My Contract",
            },
        )
    )
    result = runner.invoke(cli, ["contract-infos", "get", "ci001", "--output", "json"])
    assert result.exit_code == 0
    assert "ci001" in result.output


@respx.mock
def test_get_contract_info_not_found(runner):
    """Test getting non-existent contract info."""
    respx.get("https://api.sigfox.com/v2/contract-infos/invalid").mock(
        return_value=httpx.Response(404, json={"message": "Not Found"})
    )
    result = runner.invoke(cli, ["contract-infos", "get", "invalid"])
    assert result.exit_code != 0


# --- List Devices ---


@respx.mock
def test_list_contract_devices(runner):
    """Test listing devices for a contract."""
    respx.get("https://api.sigfox.com/v2/contract-infos/ci001/devices").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [
                    {"id": "DEV001", "name": "Device 1", "state": 0},
                    {"id": "DEV002", "name": "Device 2", "state": 0},
                ]
            },
        )
    )
    result = runner.invoke(cli, ["contract-infos", "list-devices", "ci001"])
    assert result.exit_code == 0
    assert "DEV001" in result.output


@respx.mock
def test_list_contract_devices_empty(runner):
    """Test listing devices for a contract when none exist."""
    respx.get("https://api.sigfox.com/v2/contract-infos/ci001/devices").mock(
        return_value=httpx.Response(200, json={"data": []})
    )
    result = runner.invoke(cli, ["contract-infos", "list-devices", "ci001"])
    assert result.exit_code == 0
    assert "No devices found" in result.output


@respx.mock
def test_list_contract_devices_json(runner):
    """Test listing devices for a contract in JSON format."""
    respx.get("https://api.sigfox.com/v2/contract-infos/ci001/devices").mock(
        return_value=httpx.Response(
            200,
            json={"data": [{"id": "DEV001", "name": "Device 1"}]},
        )
    )
    result = runner.invoke(
        cli, ["contract-infos", "list-devices", "ci001", "--output", "json"]
    )
    assert result.exit_code == 0
    assert "DEV001" in result.output
