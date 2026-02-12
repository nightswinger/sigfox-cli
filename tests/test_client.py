"""Tests for Sigfox API client."""

import pytest
import respx
import httpx
from sigfox_cli.client import SigfoxClient
from sigfox_cli.exceptions import (
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    APIError,
)


@pytest.fixture
def client():
    """Create a test client."""
    return SigfoxClient(
        api_login="test_login",
        api_password="test_password",
        base_url="https://api.sigfox.com/v2",
    )


@respx.mock
def test_get_success(client):
    """Test successful GET request."""
    respx.get("https://api.sigfox.com/v2/devices/").mock(
        return_value=httpx.Response(
            200,
            json={"data": [{"id": "123", "name": "Test Device"}]},
        )
    )

    response = client.get("/devices/")
    assert response["data"][0]["id"] == "123"
    assert response["data"][0]["name"] == "Test Device"


@respx.mock
def test_get_authentication_error(client):
    """Test GET request with authentication error."""
    respx.get("https://api.sigfox.com/v2/devices/").mock(
        return_value=httpx.Response(
            401,
            json={"message": "Unauthorized"},
        )
    )

    with pytest.raises(AuthenticationError):
        client.get("/devices/")


@respx.mock
def test_get_authorization_error(client):
    """Test GET request with authorization error."""
    respx.get("https://api.sigfox.com/v2/devices/123").mock(
        return_value=httpx.Response(
            403,
            json={"message": "Forbidden"},
        )
    )

    with pytest.raises(AuthorizationError):
        client.get("/devices/123")


@respx.mock
def test_get_not_found_error(client):
    """Test GET request with not found error."""
    respx.get("https://api.sigfox.com/v2/devices/999").mock(
        return_value=httpx.Response(
            404,
            json={"message": "Not Found"},
        )
    )

    with pytest.raises(NotFoundError):
        client.get("/devices/999")


@respx.mock
def test_get_api_error(client):
    """Test GET request with generic API error."""
    respx.get("https://api.sigfox.com/v2/devices/").mock(
        return_value=httpx.Response(
            500,
            json={"message": "Internal Server Error"},
        )
    )

    with pytest.raises(APIError):
        client.get("/devices/")


@respx.mock
def test_context_manager(client):
    """Test client as context manager."""
    respx.get("https://api.sigfox.com/v2/devices/").mock(
        return_value=httpx.Response(
            200,
            json={"data": []},
        )
    )

    with client as c:
        response = c.get("/devices/")
        assert "data" in response
