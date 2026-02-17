"""Tests for Users API layer."""

import httpx
import pytest
import respx

from sigfox import Sigfox
from sigfox.models import UserCreate, UserUpdate


@pytest.fixture
def sigfox_client():
    """Create a Sigfox client for testing."""
    return Sigfox(login="test_login", password="test_password")


@respx.mock
def test_users_list(sigfox_client):
    """Test UsersAPI.list() returns User objects."""
    respx.get("https://api.sigfox.com/v2/users/").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [
                    {
                        "id": "usr001",
                        "firstName": "John",
                        "lastName": "Doe",
                        "email": "john.doe@example.com",
                        "timezone": "Europe/Paris",
                    }
                ]
            },
        )
    )

    with sigfox_client as client:
        users = client.users.list()
        assert len(users) == 1
        assert users[0].id == "usr001"
        assert users[0].first_name == "John"
        assert users[0].last_name == "Doe"


@respx.mock
def test_users_get(sigfox_client):
    """Test UsersAPI.get() returns a User."""
    respx.get("https://api.sigfox.com/v2/users/usr001").mock(
        return_value=httpx.Response(
            200,
            json={
                "id": "usr001",
                "firstName": "John",
                "lastName": "Doe",
                "email": "john.doe@example.com",
                "timezone": "Europe/Paris",
            },
        )
    )

    with sigfox_client as client:
        user = client.users.get("usr001")
        assert user.id == "usr001"
        assert user.first_name == "John"
        assert user.timezone == "Europe/Paris"


@respx.mock
def test_users_create(sigfox_client):
    """Test UsersAPI.create() returns id dict."""
    respx.post("https://api.sigfox.com/v2/users/").mock(
        return_value=httpx.Response(201, json={"id": "newusr001"})
    )

    with sigfox_client as client:
        data = UserCreate(
            group_id="grp001",
            first_name="Jane",
            last_name="Smith",
            email="jane.smith@example.com",
            timezone="Europe/Paris",
            role_ids=["role001", "role002"],
        )
        result = client.users.create(data)
        assert result["id"] == "newusr001"


@respx.mock
def test_users_update(sigfox_client):
    """Test UsersAPI.update() completes without error."""
    respx.put("https://api.sigfox.com/v2/users/usr001").mock(
        return_value=httpx.Response(204)
    )

    with sigfox_client as client:
        data = UserUpdate(first_name="Jane")
        client.users.update("usr001", data)  # Should not raise


@respx.mock
def test_users_delete(sigfox_client):
    """Test UsersAPI.delete() completes without error."""
    respx.delete("https://api.sigfox.com/v2/users/usr001").mock(
        return_value=httpx.Response(204)
    )

    with sigfox_client as client:
        client.users.delete("usr001")  # Should not raise


@respx.mock
def test_users_add_roles(sigfox_client):
    """Test UsersAPI.add_roles() completes without error."""
    respx.put("https://api.sigfox.com/v2/users/usr001/roles").mock(
        return_value=httpx.Response(204)
    )

    with sigfox_client as client:
        client.users.add_roles("usr001", ["role001", "role002"])


@respx.mock
def test_users_remove_role(sigfox_client):
    """Test UsersAPI.remove_role() completes without error."""
    respx.delete("https://api.sigfox.com/v2/users/usr001/roles/role001").mock(
        return_value=httpx.Response(204)
    )

    with sigfox_client as client:
        client.users.remove_role("usr001", "role001")
