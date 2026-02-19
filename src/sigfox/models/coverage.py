"""Coverage models for Sigfox API."""

from pydantic import BaseModel, ConfigDict, Field


class CoverageLocation(BaseModel):
    """A single lat/lng coordinate for bulk coverage requests."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    lat: float
    lng: float


class CoveragePrediction(BaseModel):
    """Coverage prediction for a single location.

    Maps to the response of GET /coverages/global/predictions.
    margins[0] = margin for 1 base station redundancy
    margins[1] = margin for 2 base station redundancy
    margins[2] = margin for 3+ base station redundancy
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    location_covered: bool | None = Field(None, alias="locationCovered")
    margins: list[int] | None = None


class CoverageBulkRequest(BaseModel):
    """Request body for POST /coverages/global/predictions/bulk."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    locations: list[CoverageLocation]
    radius: int | None = None
    group_id: str | None = Field(None, alias="groupId")


class CoverageBulkResult(BaseModel):
    """Coverage prediction result for one location in a bulk response."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    lat: float | None = None
    lng: float | None = None
    location_covered: bool | None = Field(None, alias="locationCovered")
    margins: list[int] | None = None


class CoverageBulkResponse(BaseModel):
    """Response body for GET /coverages/global/predictions/bulk/{jobId}.

    jobDone is False if the job is still processing.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    job_done: bool | None = Field(None, alias="jobDone")
    time: int | None = None
    results: list[CoverageBulkResult] | None = None


class CoverageRedundancy(BaseModel):
    """Operator redundancy coverage for a location.

    Maps to the response of GET /coverages/operators/redundancy.
    redundancy: 0=no coverage, 1=1 BS, 2=2 BSs, 3=3+ BSs
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    redundancy: int | None = None
