import json
from pathlib import Path
from unittest.mock import patch

from app.pipeline.scrapers.nhtsa_vpic import NhtsaVpicApiClient

FIXTURE = Path(__file__).parent / "fixtures" / "real_pages" / "vpic_aston_martin_models.json"
ENDPOINT = "https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMakeId/440?format=json"


def test_parse_response_against_real_fixture():
    data = json.loads(FIXTURE.read_text())
    cars = NhtsaVpicApiClient.parse_response(data, ENDPOINT)

    assert len(cars) == 18
    models = {c.model for c in cars}
    assert "DB11" in models
    assert "Valhalla" in models

    db11 = next(c for c in cars if c.model == "DB11")
    assert len(db11.variants) == 1
    assert db11.variants[0].variant_name == "Base"
    assert db11.variants[0].price is None  # honest: vPIC has no pricing data
    assert db11.variants[0].source_url == ENDPOINT


def test_parse_response_deduplicates_repeated_model_names():
    data = {
        "Results": [
            {"Model_Name": "DB11"},
            {"Model_Name": "DB11"},  # vPIC sometimes has multiple rows per model (different years/subtypes)
            {"Model_Name": "Vantage"},
        ]
    }
    cars = NhtsaVpicApiClient.parse_response(data, ENDPOINT)
    assert [c.model for c in cars] == ["DB11", "Vantage"]


def test_parse_response_handles_empty_results():
    assert NhtsaVpicApiClient.parse_response({"Results": []}, ENDPOINT) == []


def test_parse_response_skips_rows_without_model_name():
    data = {"Results": [{"Make_ID": 440}, {"Model_Name": "DB11"}]}
    cars = NhtsaVpicApiClient.parse_response(data, ENDPOINT)
    assert [c.model for c in cars] == ["DB11"]


def test_scrape_end_to_end_with_fetch_mocked():
    client = NhtsaVpicApiClient(api_endpoint=ENDPOINT)
    data = json.loads(FIXTURE.read_text())

    with patch.object(NhtsaVpicApiClient, "fetch_json", return_value=data):
        cars = client.scrape()

    assert len(cars) == 18
    assert client.api_endpoint == ENDPOINT
