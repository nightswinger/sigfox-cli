"""Users API."""

from __future__ import annotations

from typing import Any

from ..client import SigfoxClient
from ..models import User, UserCreate, UserUpdate


class UsersAPI:
    """High-level API for Sigfox users (portal users)."""

    def __init__(self, client: SigfoxClient):
        self._client = client

    def list(
        self,
        limit: int | None = None,
        offset: int | None = None,
        group_ids: list[str] | None = None,
        deep: bool = False,
        fields: str | None = None,
        sort: str | None = None,
        authorizations: bool = False,
    ) -> list[User]:
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if group_ids:
            params["groupIds"] = ",".join(group_ids)
        if deep:
            params["deep"] = "true"
        if fields:
            params["fields"] = fields
        if sort:
            params["sort"] = sort
        if authorizations:
            params["authorizations"] = "true"

        response = self._client.get("/users/", params=params)
        users_data = response.get("data", [])
        return [User.model_validate(u) for u in users_data]

    def get(
        self,
        user_id: str,
        fields: str | None = None,
        authorizations: bool = False,
    ) -> User:
        params: dict[str, Any] = {}
        if fields:
            params["fields"] = fields
        if authorizations:
            params["authorizations"] = "true"

        response = self._client.get(f"/users/{user_id}", params=params or None)
        return User.model_validate(response)

    def create(self, data: UserCreate) -> dict[str, Any]:
        body = data.model_dump(by_alias=True, exclude_none=True)
        response = self._client.post("/users/", data=body)
        return response

    def update(self, user_id: str, data: UserUpdate) -> None:
        body = data.model_dump(by_alias=True, exclude_none=True)
        self._client.put(f"/users/{user_id}", data=body)

    def delete(self, user_id: str) -> None:
        self._client.delete(f"/users/{user_id}")

    def add_roles(self, user_id: str, role_ids: list[str]) -> None:
        body = {"roleIds": role_ids}
        self._client.put(f"/users/{user_id}/roles", data=body)

    def remove_role(self, user_id: str, role_id: str) -> None:
        self._client.delete(f"/users/{user_id}/roles/{role_id}")
