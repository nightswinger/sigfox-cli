"""Base Stations API."""

from __future__ import annotations

from typing import Any

from ..client import SigfoxClient
from ..models import Message


class BaseStationsAPI:
    """High-level API for Sigfox base stations."""

    def __init__(self, client: SigfoxClient):
        """Initialize Base Stations API.

        Args:
            client: Low-level Sigfox API client
        """
        self._client = client

    def list_messages(
        self,
        station_id: str,
        fields: str | None = None,
        since: int | None = None,
        before: int | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[Message]:
        """Retrieve messages received by a base station.

        Args:
            station_id: Base station identifier (hexadecimal format)
            fields: Additional fields to return. Options:
                - oob
                - ackRequired
                - device(name)
                - rinfos(cbStatus,rep,repetitions,baseStation(name))
                - downlinkAnswerStatus(baseStation(name))
            since: Starting timestamp (milliseconds since Unix epoch)
            before: Ending timestamp (milliseconds since Unix epoch)
            limit: Maximum number of messages to return (default: 100)
            offset: Number of messages to skip

        Returns:
            List of Message objects received by the base station
        """
        params: dict[str, Any] = {}
        if fields:
            params["fields"] = fields
        if since is not None:
            params["since"] = since
        if before is not None:
            params["before"] = before
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset

        response = self._client.get(
            f"/base-stations/{station_id}/messages", params=params or None
        )
        messages_data = response.get("data", [])
        return [Message.model_validate(m) for m in messages_data]
