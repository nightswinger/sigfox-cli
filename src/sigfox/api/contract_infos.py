"""Contract Infos API."""

from __future__ import annotations

from typing import Any

from ..client import SigfoxClient
from ..models import ContractInfo


class ContractInfosAPI:
    """High-level API for Sigfox contract infos."""

    def __init__(self, client: SigfoxClient):
        self._client = client

    def list(
        self,
        limit: int | None = None,
        offset: int | None = None,
        name: str | None = None,
        group_id: str | None = None,
        group_type: int | None = None,
        deep: bool = False,
        up: bool = False,
        order_ids: str | None = None,
        contract_ids: str | None = None,
        from_time: int | None = None,
        to_time: int | None = None,
        token_duration: int | None = None,
        pricing_model: int | None = None,
        subscription_plan: int | None = None,
        fields: str | None = None,
        authorizations: bool = False,
        page_id: str | None = None,
    ) -> list[ContractInfo]:
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if name:
            params["name"] = name
        if group_id:
            params["groupId"] = group_id
        if group_type is not None:
            params["groupType"] = group_type
        if deep:
            params["deep"] = "true"
        if up:
            params["up"] = "true"
        if order_ids:
            params["orderIds"] = order_ids
        if contract_ids:
            params["contractIds"] = contract_ids
        if from_time is not None:
            params["fromTime"] = from_time
        if to_time is not None:
            params["toTime"] = to_time
        if token_duration is not None:
            params["tokenDuration"] = token_duration
        if pricing_model is not None:
            params["pricingModel"] = pricing_model
        if subscription_plan is not None:
            params["subscriptionPlan"] = subscription_plan
        if fields:
            params["fields"] = fields
        if authorizations:
            params["authorizations"] = "true"
        if page_id:
            params["pageId"] = page_id

        response = self._client.get("/contract-infos/", params=params)
        data = response.get("data", [])
        return [ContractInfo.model_validate(c) for c in data]

    def get(
        self,
        contract_id: str,
        fields: str | None = None,
        authorizations: bool = False,
    ) -> ContractInfo:
        params: dict[str, Any] = {}
        if fields:
            params["fields"] = fields
        if authorizations:
            params["authorizations"] = "true"

        response = self._client.get(
            f"/contract-infos/{contract_id}", params=params or None
        )
        return ContractInfo.model_validate(response)

    def list_devices(
        self,
        contract_id: str,
        device_type_id: str | None = None,
        fields: str | None = None,
        limit: int | None = None,
        page_id: str | None = None,
    ) -> list[dict[str, Any]]:
        params: dict[str, Any] = {}
        if device_type_id:
            params["deviceTypeId"] = device_type_id
        if fields:
            params["fields"] = fields
        if limit is not None:
            params["limit"] = limit
        if page_id:
            params["pageId"] = page_id

        response = self._client.get(
            f"/contract-infos/{contract_id}/devices", params=params or None
        )
        return response.get("data", [])
