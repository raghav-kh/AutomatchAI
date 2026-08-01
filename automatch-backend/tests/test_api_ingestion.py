import json
from pathlib import Path
from unittest.mock import patch

from app.pipeline import dispatcher
from app.pipeline.scrapers.base import ScraperImportError
from app.pipeline.scrapers.nhtsa_vpic import NhtsaVpicApiClient
from app.crud import manufacturer as manufacturer_crud
from app.schemas.manufacturer import ManufacturerCreate

FIXTURE = Path(__file__).parent / "fixtures" / "real_pages" / "vpic_aston_martin_models.json"
ENDPOINT = "https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMakeId/440?format=json"


def test_instantiate_api_client_passes_endpoint(db_session):
    m = manufacturer_crud.create_manufacturer(
        db_session,
        ManufacturerCreate(
            name="Aston Martin",
            data_source_type="api",
            has_open_api=True,
            api_endpoint=ENDPOINT,
            scraper_module="app.pipeline.scrapers.nhtsa_vpic.NhtsaVpicApiClient",
        ),
    )
    source = dispatcher._instantiate_ingestion_source(m)
    assert isinstance(source, NhtsaVpicApiClient)
    assert source.api_endpoint == ENDPOINT


def test_instantiate_api_client_without_endpoint_raises_clean_error(db_session):
    m = manufacturer_crud.create_manufacturer(
        db_session,
        ManufacturerCreate(
            name="Aston Martin",
            data_source_type="api",
            scraper_module="app.pipeline.scrapers.nhtsa_vpic.NhtsaVpicApiClient",
            # api_endpoint deliberately not set
        ),
    )
    try:
        dispatcher._instantiate_ingestion_source(m)
        assert False, "expected ScraperImportError"
    except ScraperImportError as exc:
        assert "api_endpoint" in str(exc)


def test_scraper_class_still_instantiates_with_no_args(db_session):
    m = manufacturer_crud.create_manufacturer(
        db_session,
        ManufacturerCreate(
            name="Tata Motors",
            data_source_type="scraper",
            scraper_module="app.pipeline.scrapers.tata.TataScraper",
        ),
    )
    source = dispatcher._instantiate_ingestion_source(m)
    from app.pipeline.scrapers.tata import TataScraper

    assert isinstance(source, TataScraper)


def test_full_ingestion_via_api_client_persists_cars_with_provenance(db_session):
    manufacturer = manufacturer_crud.create_manufacturer(
        db_session,
        ManufacturerCreate(
            name="Aston Martin",
            data_source_type="api",
            has_open_api=True,
            api_endpoint=ENDPOINT,
            scraper_module="app.pipeline.scrapers.nhtsa_vpic.NhtsaVpicApiClient",
        ),
    )
    data = json.loads(FIXTURE.read_text())

    with patch.object(NhtsaVpicApiClient, "fetch_json", return_value=data):
        result = dispatcher.run_ingestion_for_manufacturer(db_session, manufacturer)

    assert result.cars_found == 18
    assert result.variants_saved == 18
    assert result.errors == []

    from app.models.car import Car
    from app.models.variant import Variant

    cars = db_session.query(Car).filter(Car.manufacturer_id == manufacturer.id).all()
    assert len(cars) == 18
    db11 = next(c for c in cars if c.model == "DB11")
    variants = db_session.query(Variant).filter(Variant.car_id == db11.id).all()
    assert len(variants) == 1
    assert variants[0].raw_source_url == ENDPOINT
    assert variants[0].price is None


def test_ingestion_fails_cleanly_when_api_manufacturer_missing_endpoint(db_session):
    manufacturer = manufacturer_crud.create_manufacturer(
        db_session,
        ManufacturerCreate(
            name="Aston Martin",
            data_source_type="api",
            scraper_module="app.pipeline.scrapers.nhtsa_vpic.NhtsaVpicApiClient",
        ),
    )
    result = dispatcher.run_ingestion_for_manufacturer(db_session, manufacturer)
    assert result.cars_found == 0
    assert len(result.errors) == 1
    assert "api_endpoint" in result.errors[0]
