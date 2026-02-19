"""Coverages API."""

from __future__ import annotations

from typing import Any

from ..client import SigfoxClient
from ..models import (
    CoverageBulkRequest,
    CoverageBulkResponse,
    CoveragePrediction,
    CoverageRedundancy,
)


class CoveragesAPI:
    """High-level API for Sigfox coverage predictions."""

    def __init__(self, client: SigfoxClient):
        """Initialize Coverages API.

        Args:
            client: Low-level Sigfox API client
        """
        self._client = client

    def get_global_prediction(
        self,
        lat: float,
        lng: float,
        radius: int | None = None,
        group_id: str | None = None,
    ) -> CoveragePrediction:
        """Get coverage prediction for a single location.

        Args:
            lat: Latitude in degrees (WGS 84)
            lng: Longitude in degrees (WGS 84)
            radius: Estimated radius of the device location (meters)
            group_id: Filter by group ID

        Returns:
            CoveragePrediction object
        """
        params: dict[str, Any] = {"lat": lat, "lng": lng}
        if radius is not None:
            params["radius"] = radius
        if group_id is not None:
            params["groupId"] = group_id

        response = self._client.get("/coverages/global/predictions", params=params)
        return CoveragePrediction.model_validate(response)

    def start_bulk_prediction(self, data: CoverageBulkRequest) -> dict[str, Any]:
        """Start an async bulk coverage prediction job.

        Args:
            data: Bulk request with list of locations

        Returns:
            Dict with 'jobId' of the created job
        """
        body = data.model_dump(by_alias=True, exclude_none=True)
        response = self._client.post("/coverages/global/predictions/bulk", data=body)
        return response

    def get_bulk_prediction(self, job_id: str) -> CoverageBulkResponse:
        """Get results of a bulk coverage prediction job.

        Args:
            job_id: Job ID returned by start_bulk_prediction

        Returns:
            CoverageBulkResponse object (check jobDone before using results)
        """
        response = self._client.get(
            f"/coverages/global/predictions/bulk/{job_id}"
        )
        return CoverageBulkResponse.model_validate(response)

    def get_operator_redundancy(
        self,
        lat: float,
        lng: float,
        operator_id: str | None = None,
        device_situation: str | None = None,
        device_class_id: int | None = None,
    ) -> CoverageRedundancy:
        """Get operator redundancy coverage for a location.

        Args:
            lat: Latitude in degrees (WGS 84)
            lng: Longitude in degrees (WGS 84)
            operator_id: Operator group ID (required for root Sigfox users)
            device_situation: Device installation context
                ("OUTDOOR", "INDOOR", or "UNDERGROUND")
            device_class_id: Sigfox device class (0u, 1u, 2u, 3u)

        Returns:
            CoverageRedundancy object with redundancy count
        """
        params: dict[str, Any] = {"lat": lat, "lng": lng}
        if operator_id is not None:
            params["operatorId"] = operator_id
        if device_situation is not None:
            params["deviceSituation"] = device_situation
        if device_class_id is not None:
            params["deviceClassId"] = device_class_id

        response = self._client.get("/coverages/operators/redundancy", params=params)
        return CoverageRedundancy.model_validate(response)
