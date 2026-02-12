"""Tests for SigfoxClient PUT and DELETE methods."""

import pytest
import respx
import httpx
from sigfox_cli.client import SigfoxClient
from sigfox_cli.exceptions import NotFoundError, APIError


@pytest.fixture
def client():
    """Create a test client."""
    return SigfoxClient(
        api_login="test_login",
        api_password="test_password",
        base_url="https://api.sigfox.com/v2",
    )


@respx.mock
def test_put_success_204(client):
    """Test successful PUT request with 204 No Content."""
    respx.put("https://api.sigfox.com/v2/device-types/abc123").mock(
        return_value=httpx.Response(204)
    )

    result = client.put("/device-types/abc123", data={"name": "Updated"})
    assert result == {}


@respx.mock
def test_put_success_with_json_response(client):
    """Test PUT request that returns JSON body."""
    respx.put("https://api.sigfox.com/v2/device-types/abc123").mock(
        return_value=httpx.Response(200, json={"id": "abc123", "name": "Updated"})
    )

    result = client.put("/device-types/abc123", data={"name": "Updated"})
    assert result["id"] == "abc123"
    assert result["name"] == "Updated"


@respx.mock
def test_put_not_found(client):
    """Test PUT request with not found error."""
    respx.put("https://api.sigfox.com/v2/device-types/invalid").mock(
        return_value=httpx.Response(404, json={"message": "Not Found"})
    )

    with pytest.raises(NotFoundError):
        client.put("/device-types/invalid", data={"name": "Test"})


@respx.mock
def test_put_api_error(client):
    """Test PUT request with API error."""
    respx.put("https://api.sigfox.com/v2/device-types/abc123").mock(
        return_value=httpx.Response(500, json={"message": "Internal Server Error"})
    )

    with pytest.raises(APIError):
        client.put("/device-types/abc123", data={"name": "Test"})


@respx.mock
def test_delete_success_204(client):
    """Test successful DELETE request with 204 No Content."""
    respx.delete("https://api.sigfox.com/v2/device-types/abc123").mock(
        return_value=httpx.Response(204)
    )

    result = client.delete("/device-types/abc123")
    assert result == {}


@respx.mock
def test_delete_success_with_empty_body(client):
    """Test DELETE request with empty response body."""
    respx.delete("https://api.sigfox.com/v2/device-types/abc123").mock(
        return_value=httpx.Response(200, content=b"")
    )

    result = client.delete("/device-types/abc123")
    assert result == {}


@respx.mock
def test_delete_not_found(client):
    """Test DELETE request with not found error."""
    respx.delete("https://api.sigfox.com/v2/device-types/invalid").mock(
        return_value=httpx.Response(404, json={"message": "Not Found"})
    )

    with pytest.raises(NotFoundError):
        client.delete("/device-types/invalid")


@respx.mock
def test_delete_api_error(client):
    """Test DELETE request with API error."""
    respx.delete("https://api.sigfox.com/v2/device-types/abc123").mock(
        return_value=httpx.Response(500, json={"message": "Internal Server Error"})
    )

    with pytest.raises(APIError):
        client.delete("/device-types/abc123")


@respx.mock
def test_put_with_params(client):
    """Test PUT request with query parameters."""
    respx.put("https://api.sigfox.com/v2/device-types/abc123").mock(
        return_value=httpx.Response(204)
    )

    result = client.put("/device-types/abc123", data={"name": "Test"}, params={"force": "true"})
    assert result == {}


@respx.mock
def test_delete_with_params(client):
    """Test DELETE request with query parameters."""
    respx.delete("https://api.sigfox.com/v2/device-types/abc123").mock(
        return_value=httpx.Response(204)
    )

    result = client.delete("/device-types/abc123", params={"force": "true"})
    assert result == {}
