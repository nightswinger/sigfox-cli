"""Tests for coverages commands."""

import pytest
import respx
import httpx
from click.testing import CliRunner

from sigfox_cli.app import cli


@pytest.fixture
def runner():
    """Create a CLI test runner."""
    return CliRunner()


@pytest.fixture(autouse=True)
def mock_config(monkeypatch):
    """Mock configuration to avoid reading real config files."""
    monkeypatch.setenv("SIGFOX_API_LOGIN", "test_login")
    monkeypatch.setenv("SIGFOX_API_PASSWORD", "test_password")


# --- Global Prediction ---

@respx.mock
def test_global_prediction(runner):
    """Test getting global coverage prediction."""
    respx.get("https://api.sigfox.com/v2/coverages/global/predictions").mock(
        return_value=httpx.Response(
            200,
            json={"locationCovered": True, "margins": [10, 5, -2]},
        )
    )

    result = runner.invoke(cli, ["coverages", "global-prediction", "--lat", "48.8566", "--lng", "2.3522"])
    assert result.exit_code == 0
    assert "Location Covered" in result.output


@respx.mock
def test_global_prediction_json(runner):
    """Test getting global coverage prediction in JSON format."""
    respx.get("https://api.sigfox.com/v2/coverages/global/predictions").mock(
        return_value=httpx.Response(
            200,
            json={"locationCovered": True, "margins": [10, 5, -2]},
        )
    )

    result = runner.invoke(
        cli,
        ["coverages", "global-prediction", "--lat", "48.8566", "--lng", "2.3522", "--output", "json"],
    )
    assert result.exit_code == 0
    assert "locationCovered" in result.output


def test_global_prediction_missing_lat(runner):
    """Test global-prediction fails without required --lat."""
    result = runner.invoke(cli, ["coverages", "global-prediction", "--lng", "2.3522"])
    assert result.exit_code != 0


# --- Bulk Start ---

@respx.mock
def test_bulk_start(runner):
    """Test starting a bulk coverage prediction job."""
    respx.post("https://api.sigfox.com/v2/coverages/global/predictions/bulk").mock(
        return_value=httpx.Response(202, json={"jobId": "job123"})
    )

    result = runner.invoke(
        cli,
        ["coverages", "bulk-start", "--locations", '[{"lat": 48.86, "lng": 2.35}]'],
    )
    assert result.exit_code == 0
    assert "job123" in result.output


def test_bulk_start_invalid_json(runner):
    """Test bulk-start fails with invalid JSON locations."""
    result = runner.invoke(cli, ["coverages", "bulk-start", "--locations", "not-json"])
    assert result.exit_code != 0


# --- Bulk Get ---

@respx.mock
def test_bulk_get_done(runner):
    """Test getting bulk coverage prediction results when job is done."""
    respx.get("https://api.sigfox.com/v2/coverages/global/predictions/bulk/job123").mock(
        return_value=httpx.Response(
            200,
            json={
                "jobDone": True,
                "results": [
                    {"lat": 48.86, "lng": 2.35, "locationCovered": True, "margins": [10, 5, -2]},
                ],
            },
        )
    )

    result = runner.invoke(cli, ["coverages", "bulk-get", "job123"])
    assert result.exit_code == 0
    assert "48.86" in result.output


@respx.mock
def test_bulk_get_pending(runner):
    """Test getting bulk coverage prediction when job is still processing."""
    respx.get("https://api.sigfox.com/v2/coverages/global/predictions/bulk/job123").mock(
        return_value=httpx.Response(200, json={"jobDone": False})
    )

    result = runner.invoke(cli, ["coverages", "bulk-get", "job123"])
    assert result.exit_code == 0
    assert "processing" in result.output.lower() or "still" in result.output.lower()


# --- Operator Redundancy ---

@respx.mock
def test_operator_redundancy(runner):
    """Test getting operator redundancy coverage."""
    respx.get("https://api.sigfox.com/v2/coverages/operators/redundancy").mock(
        return_value=httpx.Response(200, json={"redundancy": 3})
    )

    result = runner.invoke(
        cli,
        ["coverages", "operator-redundancy", "--lat", "48.8566", "--lng", "2.3522"],
    )
    assert result.exit_code == 0
    assert "Redundancy" in result.output


@respx.mock
def test_operator_redundancy_json(runner):
    """Test operator redundancy in JSON format."""
    respx.get("https://api.sigfox.com/v2/coverages/operators/redundancy").mock(
        return_value=httpx.Response(200, json={"redundancy": 2})
    )

    result = runner.invoke(
        cli,
        ["coverages", "operator-redundancy", "--lat", "48.8566", "--lng", "2.3522", "--output", "json"],
    )
    assert result.exit_code == 0
    assert "redundancy" in result.output


@respx.mock
def test_operator_redundancy_with_options(runner):
    """Test operator redundancy with optional parameters."""
    respx.get("https://api.sigfox.com/v2/coverages/operators/redundancy").mock(
        return_value=httpx.Response(200, json={"redundancy": 1})
    )

    result = runner.invoke(
        cli,
        [
            "coverages", "operator-redundancy",
            "--lat", "48.8566",
            "--lng", "2.3522",
            "--device-situation", "INDOOR",
            "--operator-id", "op001",
        ],
    )
    assert result.exit_code == 0


def test_operator_redundancy_missing_lat(runner):
    """Test operator-redundancy fails without required --lat."""
    result = runner.invoke(cli, ["coverages", "operator-redundancy", "--lng", "2.3522"])
    assert result.exit_code != 0
