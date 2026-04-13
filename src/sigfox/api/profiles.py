"""Profiles API."""

from __future__ import annotations

from typing import Any

from ..client import SigfoxClient
from ..models import Profile


class ProfilesAPI:
    """High-level API for Sigfox profiles."""

    def __init__(self, client: SigfoxClient):
        self._client = client

    def list(
        self,
        group_id: str,
        inherit: bool = False,
        fields: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        authorizations: bool = False,
    ) -> list[Profile]:
        params: dict[str, Any] = {"groupId": group_id}
        if inherit:
            params["inherit"] = "true"
        if fields:
            params["fields"] = fields
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if authorizations:
            params["authorizations"] = "true"

        response = self._client.get("/profiles/", params=params)
        data = response.get("data", [])
        return [Profile.model_validate(p) for p in data]

    def get(
        self,
        profile_id: str,
        fields: str | None = None,
        authorizations: bool = False,
    ) -> Profile:
        params: dict[str, Any] = {}
        if fields:
            params["fields"] = fields
        if authorizations:
            params["authorizations"] = "true"

        response = self._client.get(
            f"/profiles/{profile_id}", params=params or None
        )
        return Profile.model_validate(response)
