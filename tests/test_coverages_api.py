"""Tests for Coverages API layer."""

import pytest
import respx
import httpx

from sigfox import Sigfox
from sigfox.models import CoverageBulkRequest, CoverageLocation


@pytest.fixture
def sigfox_client():
    """Create a Sigfox client for testing."""
    return Sigfox(login="test_login", password="test_password")


@respx.mock
def test_get_global_prediction(sigfox_client):
    """Test CoveragesAPI.get_global_prediction() returns a CoveragePrediction."""
    respx.get("https://api.sigfox.com/v2/coverages/global/predictions").mock(
        return_value=httpx.Response(
            200,
            json={"locationCovered": True, "margins": [10, 5, -2]},
        )
    )

    with sigfox_client as client:
        result = client.coverages.get_global_prediction(lat=48.8566, lng=2.3522)
        assert result.location_covered is True
        assert result.margins == [10, 5, -2]


@respx.mock
def test_get_global_prediction_with_params(sigfox_client):
    """Test CoveragesAPI.get_global_prediction() passes optional params."""
    respx.get("https://api.sigfox.com/v2/coverages/global/predictions").mock(
        return_value=httpx.Response(
            200,
            json={"locationCovered": False, "margins": [-10, -20, -30]},
        )
    )

    with sigfox_client as client:
        result = client.coverages.get_global_prediction(
            lat=48.8566, lng=2.3522, radius=100, group_id="grp001"
        )
        assert result.location_covered is False
        assert result.margins == [-10, -20, -30]


@respx.mock
def test_start_bulk_prediction(sigfox_client):
    """Test CoveragesAPI.start_bulk_prediction() returns jobId."""
    respx.post("https://api.sigfox.com/v2/coverages/global/predictions/bulk").mock(
        return_value=httpx.Response(202, json={"jobId": "job123"})
    )

    with sigfox_client as client:
        request = CoverageBulkRequest(
            locations=[
                CoverageLocation(lat=48.8566, lng=2.3522),
                CoverageLocation(lat=51.5074, lng=-0.1278),
            ]
        )
        result = client.coverages.start_bulk_prediction(request)
        assert result["jobId"] == "job123"


@respx.mock
def test_get_bulk_prediction_done(sigfox_client):
    """Test CoveragesAPI.get_bulk_prediction() returns results when done."""
    respx.get("https://api.sigfox.com/v2/coverages/global/predictions/bulk/job123").mock(
        return_value=httpx.Response(
            200,
            json={
                "jobDone": True,
                "time": 1609459200000,
                "results": [
                    {"lat": 48.8566, "lng": 2.3522, "locationCovered": True, "margins": [10, 5, -2]},
                    {"lat": 51.5074, "lng": -0.1278, "locationCovered": False, "margins": [-5, -10, -15]},
                ],
            },
        )
    )

    with sigfox_client as client:
        result = client.coverages.get_bulk_prediction("job123")
        assert result.job_done is True
        assert result.results is not None
        assert len(result.results) == 2
        assert result.results[0].location_covered is True
        assert result.results[1].location_covered is False


@respx.mock
def test_get_bulk_prediction_pending(sigfox_client):
    """Test CoveragesAPI.get_bulk_prediction() returns jobDone=False when pending."""
    respx.get("https://api.sigfox.com/v2/coverages/global/predictions/bulk/job123").mock(
        return_value=httpx.Response(
            200,
            json={"jobDone": False},
        )
    )

    with sigfox_client as client:
        result = client.coverages.get_bulk_prediction("job123")
        assert result.job_done is False
        assert result.results is None


@respx.mock
def test_get_operator_redundancy(sigfox_client):
    """Test CoveragesAPI.get_operator_redundancy() returns a CoverageRedundancy."""
    respx.get("https://api.sigfox.com/v2/coverages/operators/redundancy").mock(
        return_value=httpx.Response(
            200,
            json={"redundancy": 3},
        )
    )

    with sigfox_client as client:
        result = client.coverages.get_operator_redundancy(lat=48.8566, lng=2.3522)
        assert result.redundancy == 3


@respx.mock
def test_get_operator_redundancy_with_params(sigfox_client):
    """Test CoveragesAPI.get_operator_redundancy() passes optional params."""
    respx.get("https://api.sigfox.com/v2/coverages/operators/redundancy").mock(
        return_value=httpx.Response(
            200,
            json={"redundancy": 1},
        )
    )

    with sigfox_client as client:
        result = client.coverages.get_operator_redundancy(
            lat=48.8566,
            lng=2.3522,
            operator_id="op001",
            device_situation="INDOOR",
            device_class_id=0,
        )
        assert result.redundancy == 1
