"""API Users API."""

from __future__ import annotations

from typing import Any

from ..client import SigfoxClient
from ..models import ApiUser, ApiUserCreate, ApiUserUpdate


class ApiUsersAPI:
    """High-level API for Sigfox API users."""

    def __init__(self, client: SigfoxClient):
        """Initialize API Users API.

        Args:
            client: Low-level Sigfox API client
        """
        self._client = client

    def list(
        self,
        limit: int | None = None,
        offset: int | None = None,
        profile_id: str | None = None,
        group_ids: list[str] | None = None,
        fields: str | None = None,
        authorizations: bool = False,
    ) -> list[ApiUser]:
        """List API users.

        Args:
            limit: Maximum number of API users to return
            offset: Number of API users to skip
            profile_id: Filter by profile ID
            group_ids: Filter by group IDs
            fields: Additional fields to return
            authorizations: If true, return user actions/resources

        Returns:
            List of ApiUser objects
        """
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if profile_id:
            params["profileId"] = profile_id
        if group_ids:
            params["groupIds"] = ",".join(group_ids)
        if fields:
            params["fields"] = fields
        if authorizations:
            params["authorizations"] = "true"

        response = self._client.get("/api-users/", params=params)
        users_data = response.get("data", [])
        return [ApiUser.model_validate(u) for u in users_data]

    def get(
        self,
        api_user_id: str,
        fields: str | None = None,
        authorizations: bool = False,
    ) -> ApiUser:
        """Get API user details.

        Args:
            api_user_id: API user ID
            fields: Additional fields to return
            authorizations: If true, return user actions/resources

        Returns:
            ApiUser object
        """
        params: dict[str, Any] = {}
        if fields:
            params["fields"] = fields
        if authorizations:
            params["authorizations"] = "true"

        response = self._client.get(
            f"/api-users/{api_user_id}", params=params or None
        )
        return ApiUser.model_validate(response)

    def create(self, data: ApiUserCreate) -> dict[str, Any]:
        """Create a new API user.

        Args:
            data: API user creation data

        Returns:
            Dict with 'id' of the created API user
        """
        body = data.model_dump(by_alias=True, exclude_none=True)
        response = self._client.post("/api-users/", data=body)
        return response

    def update(self, api_user_id: str, data: ApiUserUpdate) -> None:
        """Update an API user.

        Args:
            api_user_id: API user ID
            data: API user update data
        """
        body = data.model_dump(by_alias=True, exclude_none=True)
        self._client.put(f"/api-users/{api_user_id}", data=body)

    def delete(self, api_user_id: str) -> None:
        """Delete an API user.

        Args:
            api_user_id: API user ID
        """
        self._client.delete(f"/api-users/{api_user_id}")

    def add_profiles(self, api_user_id: str, profile_ids: list[str]) -> None:
        """Associate profiles to an API user.

        Args:
            api_user_id: API user ID
            profile_ids: List of profile IDs to associate
        """
        body = {"profileIds": profile_ids}
        self._client.put(f"/api-users/{api_user_id}/profiles", data=body)

    def remove_profile(self, api_user_id: str, profile_id: str) -> None:
        """Remove a profile association from an API user.

        Args:
            api_user_id: API user ID
            profile_id: Profile ID to remove
        """
        self._client.delete(f"/api-users/{api_user_id}/profiles/{profile_id}")

    def renew_credential(self, api_user_id: str) -> dict[str, Any]:
        """Generate a new password for an API user.

        Args:
            api_user_id: API user ID

        Returns:
            Dict with 'accessToken' containing the new password
        """
        response = self._client.put(
            f"/api-users/{api_user_id}/renew-credential"
        )
        return response
