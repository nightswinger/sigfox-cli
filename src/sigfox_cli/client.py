"""Sigfox API client."""

from typing import Any

import httpx

from .exceptions import (
    APIError,
    AuthenticationError,
    AuthorizationError,
    NetworkError,
    NotFoundError,
)


class SigfoxClient:
    """HTTP client for Sigfox API v2."""

    def __init__(
        self,
        api_login: str,
        api_password: str,
        base_url: str = "https://api.sigfox.com/v2",
        timeout: int = 30,
    ):
        """Initialize Sigfox API client.

        Args:
            api_login: Sigfox API login (ID)
            api_password: Sigfox API password (secret)
            base_url: API base URL
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip("/")
        self._client = httpx.Client(
            auth=(api_login, api_password),
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            timeout=timeout,
        )

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

    def close(self):
        """Close the HTTP client."""
        self._client.close()

    def _handle_error(self, response: httpx.Response) -> None:
        """Handle HTTP error responses.

        Args:
            response: HTTP response

        Raises:
            AuthenticationError: If status code is 401
            AuthorizationError: If status code is 403
            NotFoundError: If status code is 404
            APIError: For other error status codes
        """
        if response.is_success:
            return

        try:
            error_body = response.json()
            error_message = error_body.get("message", response.text)
        except Exception:
            error_message = response.text

        if response.status_code == 401:
            raise AuthenticationError(
                f"Authentication failed: {error_message}. "
                "Please check your API credentials."
            )
        elif response.status_code == 403:
            raise AuthorizationError(
                f"Authorization failed: {error_message}. "
                "You don't have permission to access this resource."
            )
        elif response.status_code == 404:
            raise NotFoundError(f"Resource not found: {error_message}")
        elif response.status_code >= 400:
            raise APIError(
                f"API error (status {response.status_code}): {error_message}",
                status_code=response.status_code,
                response_body=response.text,
            )

    def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Make a GET request to the API.

        Args:
            path: API endpoint path (e.g., "/devices")
            params: Query parameters

        Returns:
            Response JSON data

        Raises:
            NetworkError: If network connection fails
            AuthenticationError: If authentication fails
            APIError: If API returns an error
        """
        url = f"{self.base_url}{path}"
        try:
            response = self._client.get(url, params=params)
            self._handle_error(response)
            return response.json()
        except httpx.NetworkError as e:
            raise NetworkError(f"Network error: {e}") from e
        except httpx.TimeoutException as e:
            raise NetworkError(f"Request timeout: {e}") from e

    def post(
        self, path: str, data: dict[str, Any] | None = None, params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Make a POST request to the API.

        Args:
            path: API endpoint path
            data: Request body data
            params: Query parameters

        Returns:
            Response JSON data

        Raises:
            NetworkError: If network connection fails
            AuthenticationError: If authentication fails
            APIError: If API returns an error
        """
        url = f"{self.base_url}{path}"
        try:
            response = self._client.post(url, json=data, params=params)
            self._handle_error(response)
            return response.json()
        except httpx.NetworkError as e:
            raise NetworkError(f"Network error: {e}") from e
        except httpx.TimeoutException as e:
            raise NetworkError(f"Request timeout: {e}") from e

    def get_paginated(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        limit: int | None = None,
    ) -> list[dict[str, Any]]:
        """Get paginated results from the API.

        Args:
            path: API endpoint path
            params: Query parameters
            limit: Maximum number of items to fetch (None = all)

        Returns:
            List of all items from paginated responses

        Raises:
            NetworkError: If network connection fails
            APIError: If API returns an error
        """
        if params is None:
            params = {}

        all_items: list[dict[str, Any]] = []
        offset = params.get("offset", 0)
        page_limit = params.get("limit", 100)

        while True:
            # Update pagination params
            params["offset"] = offset
            params["limit"] = page_limit

            # Fetch page
            response_data = self.get(path, params=params)
            items = response_data.get("data", [])

            if not items:
                break

            all_items.extend(items)

            # Check if we've reached the user-specified limit
            if limit is not None and len(all_items) >= limit:
                all_items = all_items[:limit]
                break

            # Check if there are more pages
            paging = response_data.get("paging", {})
            next_url = paging.get("next")
            if not next_url:
                break

            # Update offset for next page
            offset += len(items)

        return all_items
