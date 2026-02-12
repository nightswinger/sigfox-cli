"""Device Types API."""

from __future__ import annotations

from typing import Any

from ..client import SigfoxClient
from ..models import DeviceTypeCreate, DeviceTypeModel, DeviceTypeUpdate


class DeviceTypesAPI:
    """High-level API for Sigfox device types."""

    def __init__(self, client: SigfoxClient):
        """Initialize Device Types API.

        Args:
            client: Low-level Sigfox API client
        """
        self._client = client

    def list(
        self,
        limit: int | None = None,
        offset: int | None = None,
        name: str | None = None,
        group_ids: list[str] | None = None,
        deep: bool = False,
        sort: str | None = None,
    ) -> list[DeviceTypeModel]:
        """List device types.

        Args:
            limit: Maximum number of device types to return
            offset: Number of device types to skip
            name: Filter by name (partial match)
            group_ids: Filter by group IDs
            deep: Include device types from child groups
            sort: Sort field (e.g., "name", "-creationTime")

        Returns:
            List of DeviceType objects
        """
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if name:
            params["name"] = name
        if group_ids:
            params["groupIds"] = ",".join(group_ids)
        if deep:
            params["deep"] = "true"
        if sort:
            params["sort"] = sort

        response = self._client.get("/device-types/", params=params)
        device_types_data = response.get("data", [])
        return [DeviceTypeModel.model_validate(dt) for dt in device_types_data]

    def get(self, device_type_id: str) -> DeviceTypeModel:
        """Get device type details.

        Args:
            device_type_id: Device type ID

        Returns:
            DeviceType object
        """
        response = self._client.get(f"/device-types/{device_type_id}")
        return DeviceTypeModel.model_validate(response)

    def create(self, data: DeviceTypeCreate) -> DeviceTypeModel:
        """Create a new device type.

        Args:
            data: Device type creation data

        Returns:
            Created DeviceType object
        """
        body = data.model_dump(by_alias=True, exclude_none=True)
        response = self._client.post("/device-types/", data=body)
        return DeviceTypeModel.model_validate(response)

    def update(self, device_type_id: str, data: DeviceTypeUpdate) -> None:
        """Update a device type.

        Args:
            device_type_id: Device type ID
            data: Device type update data
        """
        body = data.model_dump(by_alias=True, exclude_none=True)
        self._client.put(f"/device-types/{device_type_id}", data=body)

    def delete(self, device_type_id: str) -> None:
        """Delete a device type.

        Args:
            device_type_id: Device type ID
        """
        self._client.delete(f"/device-types/{device_type_id}")
