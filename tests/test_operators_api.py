"""Tests for Operators API layer."""

import httpx
import pytest
import respx

from sigfox import Sigfox


@pytest.fixture
def sigfox_client():
    """Create a Sigfox client for testing."""
    return Sigfox(login="test_login", password="test_password")


@respx.mock
def test_operators_list(sigfox_client):
    """Test OperatorsAPI.list() returns Operator objects."""
    respx.get("https://api.sigfox.com/v2/operators/").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [
                    {
                        "id": "op001",
                        "name": "Operator One",
                        "hostOperator": True,
                        "contractId": "contract001",
                    }
                ]
            },
        )
    )

    with sigfox_client as client:
        operators = client.operators.list()
        assert len(operators) == 1
        assert operators[0].id == "op001"
        assert operators[0].name == "Operator One"
        assert operators[0].host_operator is True
        assert operators[0].contract_id == "contract001"


@respx.mock
def test_operators_list_empty(sigfox_client):
    """Test OperatorsAPI.list() returns empty list when no operators."""
    respx.get("https://api.sigfox.com/v2/operators/").mock(
        return_value=httpx.Response(200, json={"data": []})
    )

    with sigfox_client as client:
        operators = client.operators.list()
        assert operators == []


@respx.mock
def test_operators_list_with_group(sigfox_client):
    """Test OperatorsAPI.list() maps nested group correctly."""
    respx.get("https://api.sigfox.com/v2/operators/").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [
                    {
                        "id": "op001",
                        "name": "Operator One",
                        "group": {"id": "grp001", "name": "My Group", "type": 0, "level": 1},
                    }
                ]
            },
        )
    )

    with sigfox_client as client:
        operators = client.operators.list()
        assert operators[0].group is not None
        assert operators[0].group.id == "grp001"
        assert operators[0].group.name == "My Group"


@respx.mock
def test_operators_get(sigfox_client):
    """Test OperatorsAPI.get() returns a single Operator."""
    respx.get("https://api.sigfox.com/v2/operators/op001").mock(
        return_value=httpx.Response(
            200,
            json={
                "id": "op001",
                "name": "Operator One",
                "hostOperator": False,
                "contractId": "contract001",
                "creationTime": 1609459200000,
            },
        )
    )

    with sigfox_client as client:
        operator = client.operators.get("op001")
        assert operator.id == "op001"
        assert operator.name == "Operator One"
        assert operator.host_operator is False
        assert operator.creation_time == 1609459200000
