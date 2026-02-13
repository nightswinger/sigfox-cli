"""Tests for Groups API layer."""

import pytest
import respx
import httpx

from sigfox import Sigfox
from sigfox.models import GroupCreate, GroupUpdate


@pytest.fixture
def sigfox_client():
    """Create a Sigfox client for testing."""
    return Sigfox(login="test_login", password="test_password")


@respx.mock
def test_groups_list(sigfox_client):
    """Test GroupsAPI.list() returns Group objects."""
    respx.get("https://api.sigfox.com/v2/groups/").mock(
        return_value=httpx.Response(
            200,
            json={"data": [{"id": "grp001", "name": "G1", "type": 2}]},
        )
    )

    with sigfox_client as client:
        groups = client.groups.list()
        assert len(groups) == 1
        assert groups[0].id == "grp001"
        assert groups[0].name == "G1"
        assert groups[0].type == 2


@respx.mock
def test_groups_get(sigfox_client):
    """Test GroupsAPI.get() returns a Group."""
    respx.get("https://api.sigfox.com/v2/groups/grp001").mock(
        return_value=httpx.Response(
            200,
            json={"id": "grp001", "name": "G1", "type": 2, "timezone": "Europe/Paris"},
        )
    )

    with sigfox_client as client:
        group = client.groups.get("grp001")
        assert group.id == "grp001"
        assert group.timezone == "Europe/Paris"


@respx.mock
def test_groups_create(sigfox_client):
    """Test GroupsAPI.create() returns id dict."""
    respx.post("https://api.sigfox.com/v2/groups/").mock(
        return_value=httpx.Response(201, json={"id": "newgrp001"})
    )

    with sigfox_client as client:
        data = GroupCreate(
            name="Test",
            description="Desc",
            type=8,
            timezone="Europe/Paris",
            parent_id="parent001",
        )
        result = client.groups.create(data)
        assert result["id"] == "newgrp001"


@respx.mock
def test_groups_update(sigfox_client):
    """Test GroupsAPI.update() completes without error."""
    respx.put("https://api.sigfox.com/v2/groups/grp001").mock(
        return_value=httpx.Response(204)
    )

    with sigfox_client as client:
        data = GroupUpdate(name="Updated")
        client.groups.update("grp001", data)  # Should not raise


@respx.mock
def test_groups_delete(sigfox_client):
    """Test GroupsAPI.delete() completes without error."""
    respx.delete("https://api.sigfox.com/v2/groups/grp001").mock(
        return_value=httpx.Response(204)
    )

    with sigfox_client as client:
        client.groups.delete("grp001")  # Should not raise


@respx.mock
def test_groups_callbacks_not_delivered(sigfox_client):
    """Test GroupsAPI.callbacks_not_delivered() returns error objects."""
    respx.get("https://api.sigfox.com/v2/groups/grp001/callbacks-not-delivered").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [
                    {"device": "1A2B3C", "time": 1609459200000, "status": "error"},
                ]
            },
        )
    )

    with sigfox_client as client:
        errors = client.groups.callbacks_not_delivered("grp001")
        assert len(errors) == 1
        assert errors[0].device == "1A2B3C"


@respx.mock
def test_groups_geoloc_payloads(sigfox_client):
    """Test GroupsAPI.geoloc_payloads() returns payload objects."""
    respx.get("https://api.sigfox.com/v2/groups/grp001/geoloc-payloads").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [
                    {"id": "geo001", "name": "Payload A"},
                ]
            },
        )
    )

    with sigfox_client as client:
        payloads = client.groups.geoloc_payloads("grp001")
        assert len(payloads) == 1
        assert payloads[0].id == "geo001"
