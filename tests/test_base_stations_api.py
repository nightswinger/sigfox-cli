"""Tests for base stations API."""

import pytest
import httpx
import respx

from sigfox import Sigfox


@pytest.fixture
def sigfox_client():
    """Create a Sigfox client for testing."""
    return Sigfox(login="test_login", password="test_password")


@respx.mock
def test_base_stations_list_messages(sigfox_client):
    """Test BaseStationsAPI.list_messages() returns Message objects."""
    respx.get("https://api.sigfox.com/v2/base-stations/1A2B3C/messages").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [
                    {
                        "device": {"id": "AABBCC"},
                        "time": 1609459200000,
                        "data": "deadbeef",
                        "seqNumber": 1,
                    }
                ]
            },
        )
    )

    with sigfox_client as client:
        messages = client.base_stations.list_messages(station_id="1A2B3C")
        assert len(messages) == 1
        assert messages[0].device.id == "AABBCC"
        assert messages[0].time == 1609459200000


@respx.mock
def test_base_stations_list_messages_with_params(sigfox_client):
    """Test listing messages with parameters."""
    respx.get("https://api.sigfox.com/v2/base-stations/ABC123/messages").mock(
        return_value=httpx.Response(
            200,
            json={"data": []},
        )
    )

    with sigfox_client as client:
        messages = client.base_stations.list_messages(
            station_id="ABC123",
            fields="device(name)",
            since=1609459200000,
            before=1609545600000,
            limit=50,
            offset=10,
        )
        assert messages == []


@respx.mock
def test_base_stations_list_messages_with_fields(sigfox_client):
    """Test listing messages with additional fields."""
    respx.get("https://api.sigfox.com/v2/base-stations/1A2B3C/messages").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [
                    {
                        "device": {"id": "AABBCC", "name": "Test Device"},
                        "time": 1609459200000,
                        "data": "deadbeef",
                        "seqNumber": 1,
                    }
                ]
            },
        )
    )

    with sigfox_client as client:
        messages = client.base_stations.list_messages(
            station_id="1A2B3C", fields="device(name)"
        )
        assert len(messages) == 1
        assert messages[0].device.id == "AABBCC"
        assert messages[0].device.name == "Test Device"


@respx.mock
def test_base_stations_list_messages_empty(sigfox_client):
    """Test listing messages with empty response."""
    respx.get("https://api.sigfox.com/v2/base-stations/1A2B3C/messages").mock(
        return_value=httpx.Response(
            200,
            json={"data": []},
        )
    )

    with sigfox_client as client:
        messages = client.base_stations.list_messages(station_id="1A2B3C")
        assert messages == []
