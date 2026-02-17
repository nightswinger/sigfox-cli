"""Tests for API Users API layer."""

import httpx
import pytest
import respx

from sigfox import Sigfox
from sigfox.models import ApiUserCreate, ApiUserUpdate


@pytest.fixture
def sigfox_client():
    """Create a Sigfox client for testing."""
    return Sigfox(login="test_login", password="test_password")


@respx.mock
def test_api_users_list(sigfox_client):
    """Test ApiUsersAPI.list() returns ApiUser objects."""
    respx.get("https://api.sigfox.com/v2/api-users/").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [
                    {"id": "usr001", "name": "API User 1", "timezone": "Europe/Paris"}
                ]
            },
        )
    )

    with sigfox_client as client:
        users = client.api_users.list()
        assert len(users) == 1
        assert users[0].id == "usr001"
        assert users[0].name == "API User 1"


@respx.mock
def test_api_users_get(sigfox_client):
    """Test ApiUsersAPI.get() returns an ApiUser."""
    respx.get("https://api.sigfox.com/v2/api-users/usr001").mock(
        return_value=httpx.Response(
            200,
            json={"id": "usr001", "name": "API User 1", "timezone": "Europe/Paris"},
        )
    )

    with sigfox_client as client:
        user = client.api_users.get("usr001")
        assert user.id == "usr001"
        assert user.timezone == "Europe/Paris"


@respx.mock
def test_api_users_create(sigfox_client):
    """Test ApiUsersAPI.create() returns id dict."""
    respx.post("https://api.sigfox.com/v2/api-users/").mock(
        return_value=httpx.Response(201, json={"id": "newusr001"})
    )

    with sigfox_client as client:
        data = ApiUserCreate(
            group_id="grp001",
            name="Test User",
            timezone="Europe/Paris",
            profile_ids=["prof001", "prof002"],
        )
        result = client.api_users.create(data)
        assert result["id"] == "newusr001"


@respx.mock
def test_api_users_update(sigfox_client):
    """Test ApiUsersAPI.update() completes without error."""
    respx.put("https://api.sigfox.com/v2/api-users/usr001").mock(
        return_value=httpx.Response(204)
    )

    with sigfox_client as client:
        data = ApiUserUpdate(name="Updated")
        client.api_users.update("usr001", data)  # Should not raise


@respx.mock
def test_api_users_delete(sigfox_client):
    """Test ApiUsersAPI.delete() completes without error."""
    respx.delete("https://api.sigfox.com/v2/api-users/usr001").mock(
        return_value=httpx.Response(204)
    )

    with sigfox_client as client:
        client.api_users.delete("usr001")  # Should not raise


@respx.mock
def test_api_users_add_profiles(sigfox_client):
    """Test ApiUsersAPI.add_profiles() completes without error."""
    respx.put("https://api.sigfox.com/v2/api-users/usr001/profiles").mock(
        return_value=httpx.Response(204)
    )

    with sigfox_client as client:
        client.api_users.add_profiles("usr001", ["prof001", "prof002"])


@respx.mock
def test_api_users_remove_profile(sigfox_client):
    """Test ApiUsersAPI.remove_profile() completes without error."""
    respx.delete("https://api.sigfox.com/v2/api-users/usr001/profiles/prof001").mock(
        return_value=httpx.Response(204)
    )

    with sigfox_client as client:
        client.api_users.remove_profile("usr001", "prof001")


@respx.mock
def test_api_users_renew_credential(sigfox_client):
    """Test ApiUsersAPI.renew_credential() returns access token."""
    respx.put("https://api.sigfox.com/v2/api-users/usr001/renew-credential").mock(
        return_value=httpx.Response(
            200,
            json={"accessToken": "new_token_abc123"},
        )
    )

    with sigfox_client as client:
        result = client.api_users.renew_credential("usr001")
        assert result["accessToken"] == "new_token_abc123"
