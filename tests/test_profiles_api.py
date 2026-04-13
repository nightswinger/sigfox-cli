"""Tests for Profiles API layer."""

import httpx
import pytest
import respx

from sigfox import Sigfox


@pytest.fixture
def sigfox_client():
    """Create a Sigfox client for testing."""
    return Sigfox(login="test_login", password="test_password")


@respx.mock
def test_profiles_list(sigfox_client):
    """Test ProfilesAPI.list() returns Profile objects."""
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

    with sigfox_client as client:
        profiles = client.profiles.list(group_id="grp001")
        assert len(profiles) == 1
        assert profiles[0].id == "prof001"
        assert profiles[0].name == "CUSTOMER [R]"


@respx.mock
def test_profiles_list_empty(sigfox_client):
    """Test ProfilesAPI.list() returns empty list when no profiles."""
    respx.get("https://api.sigfox.com/v2/profiles/").mock(
        return_value=httpx.Response(200, json={"data": []})
    )

    with sigfox_client as client:
        profiles = client.profiles.list(group_id="grp001")
        assert profiles == []


@respx.mock
def test_profiles_list_with_group(sigfox_client):
    """Test ProfilesAPI.list() maps nested group correctly."""
    respx.get("https://api.sigfox.com/v2/profiles/").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [
                    {
                        "id": "prof001",
                        "name": "CUSTOMER [R]",
                        "group": {"id": "grp001", "name": "My Group", "type": 0, "level": 1},
                    }
                ]
            },
        )
    )

    with sigfox_client as client:
        profiles = client.profiles.list(group_id="grp001")
        assert profiles[0].group is not None
        assert profiles[0].group.id == "grp001"
        assert profiles[0].group.name == "My Group"
        assert profiles[0].group.type == 0
        assert profiles[0].group.level == 1


@respx.mock
def test_profiles_list_with_roles(sigfox_client):
    """Test ProfilesAPI.list() maps nested roles correctly."""
    respx.get("https://api.sigfox.com/v2/profiles/").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [
                    {
                        "id": "prof001",
                        "name": "CUSTOMER [R]",
                        "roles": [
                            {
                                "id": "role001",
                                "name": "Read Devices",
                                "path": [{"id": "meta001", "name": "Devices"}],
                            }
                        ],
                    }
                ]
            },
        )
    )

    with sigfox_client as client:
        profiles = client.profiles.list(group_id="grp001")
        assert profiles[0].roles is not None
        assert len(profiles[0].roles) == 1
        assert profiles[0].roles[0].id == "role001"
        assert profiles[0].roles[0].name == "Read Devices"
        assert profiles[0].roles[0].path is not None
        assert profiles[0].roles[0].path[0].name == "Devices"


@respx.mock
def test_profiles_get(sigfox_client):
    """Test ProfilesAPI.get() returns a single Profile."""
    respx.get("https://api.sigfox.com/v2/profiles/prof001").mock(
        return_value=httpx.Response(
            200,
            json={
                "id": "prof001",
                "name": "CUSTOMER [R]",
                "group": {"id": "grp001", "name": "My Group", "type": 0, "level": 1},
            },
        )
    )

    with sigfox_client as client:
        profile = client.profiles.get("prof001")
        assert profile.id == "prof001"
        assert profile.name == "CUSTOMER [R]"
        assert profile.group is not None
        assert profile.group.id == "grp001"


@respx.mock
def test_profiles_get_with_roles_and_group(sigfox_client):
    """Test ProfilesAPI.get() maps roles and group together."""
    respx.get("https://api.sigfox.com/v2/profiles/prof001").mock(
        return_value=httpx.Response(
            200,
            json={
                "id": "prof001",
                "name": "CUSTOMER [RW]",
                "group": {"id": "grp001", "name": "My Group", "type": 0, "level": 2},
                "roles": [
                    {"id": "role001", "name": "Read Devices"},
                    {"id": "role002", "name": "Write Devices"},
                ],
            },
        )
    )

    with sigfox_client as client:
        profile = client.profiles.get("prof001")
        assert profile.id == "prof001"
        assert profile.group is not None
        assert profile.group.level == 2
        assert profile.roles is not None
        assert len(profile.roles) == 2
        assert profile.roles[1].name == "Write Devices"
