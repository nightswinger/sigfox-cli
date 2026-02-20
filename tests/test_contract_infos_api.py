"""Tests for Contract Infos API layer."""

import httpx
import pytest
import respx

from sigfox import Sigfox
from sigfox.models import ContractInfo


@pytest.fixture
def sigfox_client():
    """Create a Sigfox client for testing."""
    return Sigfox(login="test_login", password="test_password")


@respx.mock
def test_contract_infos_list(sigfox_client):
    """Test ContractInfosAPI.list() returns ContractInfo objects."""
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
                        "tokenDuration": 12,
                        "maxTokens": 1000,
                        "tokensInUse": 42,
                    }
                ]
            },
        )
    )

    with sigfox_client as client:
        contracts = client.contract_infos.list()
        assert len(contracts) == 1
        assert contracts[0].id == "ci001"
        assert contracts[0].name == "My Contract"
        assert contracts[0].contract_id == "BSS-001"
        assert contracts[0].subscription_plan == 1
        assert contracts[0].tokens_in_use == 42


@respx.mock
def test_contract_infos_list_empty(sigfox_client):
    """Test ContractInfosAPI.list() returns empty list when no data."""
    respx.get("https://api.sigfox.com/v2/contract-infos/").mock(
        return_value=httpx.Response(200, json={"data": []})
    )

    with sigfox_client as client:
        contracts = client.contract_infos.list()
        assert contracts == []


@respx.mock
def test_contract_infos_list_with_filters(sigfox_client):
    """Test ContractInfosAPI.list() passes query params."""
    route = respx.get("https://api.sigfox.com/v2/contract-infos/").mock(
        return_value=httpx.Response(200, json={"data": []})
    )

    with sigfox_client as client:
        client.contract_infos.list(
            limit=10,
            offset=5,
            group_id="grp001",
            subscription_plan=1,
        )

    request = route.calls[0].request
    assert b"limit=10" in request.url.query
    assert b"groupId=grp001" in request.url.query
    assert b"subscriptionPlan=1" in request.url.query


@respx.mock
def test_contract_infos_get(sigfox_client):
    """Test ContractInfosAPI.get() returns a ContractInfo."""
    respx.get("https://api.sigfox.com/v2/contract-infos/ci001").mock(
        return_value=httpx.Response(
            200,
            json={
                "id": "ci001",
                "name": "My Contract",
                "contractId": "BSS-001",
                "pricingModel": 2,
                "startTime": 1609459200000,
                "timezone": "Europe/Paris",
                "group": {"id": "grp001", "name": "My Group"},
            },
        )
    )

    with sigfox_client as client:
        contract = client.contract_infos.get("ci001")
        assert contract.id == "ci001"
        assert contract.name == "My Contract"
        assert contract.pricing_model == 2
        assert contract.timezone == "Europe/Paris"
        assert contract.group is not None
        assert contract.group.name == "My Group"


@respx.mock
def test_contract_infos_list_devices(sigfox_client):
    """Test ContractInfosAPI.list_devices() returns device dicts."""
    respx.get("https://api.sigfox.com/v2/contract-infos/ci001/devices").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [
                    {"id": "DEV001", "name": "Device 1"},
                    {"id": "DEV002", "name": "Device 2"},
                ]
            },
        )
    )

    with sigfox_client as client:
        devices = client.contract_infos.list_devices("ci001")
        assert len(devices) == 2
        assert devices[0]["id"] == "DEV001"
        assert devices[1]["name"] == "Device 2"


@respx.mock
def test_contract_infos_list_devices_empty(sigfox_client):
    """Test ContractInfosAPI.list_devices() returns empty list."""
    respx.get("https://api.sigfox.com/v2/contract-infos/ci001/devices").mock(
        return_value=httpx.Response(200, json={"data": []})
    )

    with sigfox_client as client:
        devices = client.contract_infos.list_devices("ci001")
        assert devices == []
