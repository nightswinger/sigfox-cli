"""Groups API."""

from __future__ import annotations

from typing import Any

from ..client import SigfoxClient
from ..models import GeolocPayload, Group, GroupCallbackError, GroupCreate, GroupUpdate


class GroupsAPI:
    """High-level API for Sigfox groups."""

    def __init__(self, client: SigfoxClient):
        """Initialize Groups API.

        Args:
            client: Low-level Sigfox API client
        """
        self._client = client

    def list(
        self,
        limit: int | None = None,
        offset: int | None = None,
        parent_ids: list[str] | None = None,
        deep: bool = False,
        name: str | None = None,
        types: list[int] | None = None,
        fields: str | None = None,
        action: str | None = None,
        sort: str | None = None,
        authorizations: bool = False,
        page_id: str | None = None,
    ) -> list[Group]:
        """List groups.

        Args:
            limit: Maximum number of groups to return
            offset: Number of groups to skip
            parent_ids: Filter by parent group IDs
            deep: Retrieve all sub-groups recursively
            name: Filter by name (contains match)
            types: Filter by group types (0=SO, 2=Other, 5=SVNO, etc.)
            fields: Additional fields to return (e.g., "path(name,type,level)")
            action: Filter by resource:action pair the user has access to
            sort: Sort field ("id", "-id", "name", "-name")
            authorizations: If true, return the list of actions/resources the user can access
            page_id: Token representing the page to retrieve

        Returns:
            List of Group objects
        """
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if parent_ids:
            params["parentIds"] = ",".join(parent_ids)
        if deep:
            params["deep"] = "true"
        if name:
            params["name"] = name
        if types:
            params["types"] = ",".join(str(t) for t in types)
        if fields:
            params["fields"] = fields
        if action:
            params["action"] = action
        if sort:
            params["sort"] = sort
        if authorizations:
            params["authorizations"] = "true"
        if page_id:
            params["pageId"] = page_id

        response = self._client.get("/groups/", params=params)
        groups_data = response.get("data", [])
        return [Group.model_validate(g) for g in groups_data]

    def get(
        self,
        group_id: str,
        fields: str | None = None,
        authorizations: bool = False,
    ) -> Group:
        """Get group details.

        Args:
            group_id: Group ID
            fields: Additional fields to return (e.g., "paths(name)")
            authorizations: If true, return the list of actions/resources

        Returns:
            Group object
        """
        params: dict[str, Any] = {}
        if fields:
            params["fields"] = fields
        if authorizations:
            params["authorizations"] = "true"

        response = self._client.get(f"/groups/{group_id}", params=params or None)
        return Group.model_validate(response)

    def create(self, data: GroupCreate) -> dict[str, Any]:
        """Create a new group.

        Args:
            data: Group creation data

        Returns:
            Dict with 'id' of the created group
        """
        body = data.model_dump(by_alias=True, exclude_none=True)
        response = self._client.post("/groups/", data=body)
        return response

    def update(self, group_id: str, data: GroupUpdate) -> None:
        """Update a group.

        Args:
            group_id: Group ID
            data: Group update data
        """
        body = data.model_dump(by_alias=True, exclude_none=True)
        self._client.put(f"/groups/{group_id}", data=body)

    def delete(self, group_id: str) -> None:
        """Delete a group.

        Args:
            group_id: Group ID
        """
        self._client.delete(f"/groups/{group_id}")

    def callbacks_not_delivered(
        self,
        group_id: str,
        since: int | None = None,
        before: int | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[GroupCallbackError]:
        """Get undelivered callbacks for a group.

        Args:
            group_id: Group ID
            since: Starting timestamp (ms since Unix epoch)
            before: Ending timestamp (ms since Unix epoch)
            limit: Maximum number of items to return
            offset: Number of items to skip

        Returns:
            List of GroupCallbackError objects
        """
        params: dict[str, Any] = {}
        if since is not None:
            params["since"] = since
        if before is not None:
            params["before"] = before
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset

        response = self._client.get(
            f"/groups/{group_id}/callbacks-not-delivered", params=params
        )
        data = response.get("data", [])
        return [GroupCallbackError.model_validate(item) for item in data]

    def geoloc_payloads(
        self,
        group_id: str,
        limit: int | None = None,
        offset: int | None = None,
        page_id: str | None = None,
    ) -> list[GeolocPayload]:
        """Get geolocation payloads for a group.

        Args:
            group_id: Group ID
            limit: Maximum number of items to return
            offset: Number of items to skip
            page_id: Token for pagination

        Returns:
            List of GeolocPayload objects
        """
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if page_id:
            params["pageId"] = page_id

        response = self._client.get(
            f"/groups/{group_id}/geoloc-payloads", params=params
        )
        data = response.get("data", [])
        return [GeolocPayload.model_validate(item) for item in data]
