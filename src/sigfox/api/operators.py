"""Operators API."""

from __future__ import annotations

from typing import Any

from ..client import SigfoxClient
from ..models import Operator


class OperatorsAPI:
    """High-level API for Sigfox operators."""

    def __init__(self, client: SigfoxClient):
        self._client = client

    def list(
        self,
        limit: int | None = None,
        offset: int | None = None,
        group_ids: list[str] | None = None,
        deep: bool = False,
        fields: str | None = None,
        authorizations: bool = False,
    ) -> list[Operator]:
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
        if authorizations:
            params["authorizations"] = "true"

        response = self._client.get("/operators/", params=params)
        data = response.get("data", [])
        return [Operator.model_validate(o) for o in data]

    def get(
        self,
        operator_id: str,
        fields: str | None = None,
        authorizations: bool = False,
    ) -> Operator:
        params: dict[str, Any] = {}
        if fields:
            params["fields"] = fields
        if authorizations:
            params["authorizations"] = "true"

        response = self._client.get(
            f"/operators/{operator_id}", params=params or None
        )
        return Operator.model_validate(response)
