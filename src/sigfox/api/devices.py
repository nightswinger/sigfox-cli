"""Devices API."""

from __future__ import annotations

from typing import Any

from ..client import SigfoxClient
from ..models import Device, DeviceCreate, DeviceUpdate, Message


class DevicesAPI:
    """High-level API for Sigfox devices."""

    def __init__(self, client: SigfoxClient):
        """Initialize Devices API.

        Args:
            client: Low-level Sigfox API client
        """
        self._client = client

    def list(
        self,
        limit: int | None = None,
        offset: int | None = None,
        device_type_id: str | None = None,
        group_ids: list[str] | None = None,
        deep: bool = False,
        sort: str | None = None,
    ) -> list[Device]:
        """List devices.

        Args:
            limit: Maximum number of devices to return
            offset: Number of devices to skip
            device_type_id: Filter by device type ID
            group_ids: Filter by group IDs
            deep: Include devices from child groups
            sort: Sort field (e.g., "name", "-lastCom")

        Returns:
            List of Device objects
        """
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if device_type_id:
            params["deviceTypeId"] = device_type_id
        if group_ids:
            params["groupIds"] = ",".join(group_ids)
        if deep:
            params["deep"] = "true"
        if sort:
            params["sort"] = sort

        response = self._client.get("/devices/", params=params)
        devices_data = response.get("data", [])
        return [Device.model_validate(d) for d in devices_data]

    def get(self, device_id: str) -> Device:
        """Get device details.

        Args:
            device_id: Device ID

        Returns:
            Device object
        """
        response = self._client.get(f"/devices/{device_id}")
        return Device.model_validate(response)

    def create(self, data: DeviceCreate) -> Device:
        """Create a new device.

        Args:
            data: Device creation data

        Returns:
            Created Device object
        """
        body = data.model_dump(by_alias=True, exclude_none=True)
        response = self._client.post("/devices/", data=body)
        return Device.model_validate(response)

    def update(self, device_id: str, data: DeviceUpdate) -> None:
        """Update a device.

        Args:
            device_id: Device ID
            data: Device update data
        """
        body = data.model_dump(by_alias=True, exclude_none=True)
        self._client.put(f"/devices/{device_id}", data=body)

    def delete(self, device_id: str) -> None:
        """Delete a device.

        Args:
            device_id: Device ID
        """
        self._client.delete(f"/devices/{device_id}")

    def messages(
        self,
        device_id: str,
        limit: int | None = None,
        offset: int | None = None,
        since: int | None = None,
        before: int | None = None,
    ) -> list[Message]:
        """Get messages for a device.

        Args:
            device_id: Device ID
            limit: Maximum number of messages to return
            offset: Number of messages to skip
            since: Unix timestamp (ms) - only messages after this time
            before: Unix timestamp (ms) - only messages before this time

        Returns:
            List of Message objects
        """
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if since is not None:
            params["since"] = since
        if before is not None:
            params["before"] = before

        response = self._client.get(f"/devices/{device_id}/messages", params=params)
        messages_data = response.get("data", [])
        return [Message.model_validate(m) for m in messages_data]
