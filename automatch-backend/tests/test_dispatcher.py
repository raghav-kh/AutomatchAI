import httpx

from app.pipeline import dispatcher
from app.crud import manufacturer as manufacturer_crud
from app.schemas.manufacturer import ManufacturerCreate, ManufacturerUpdate
from app.models.manufacturer import DataSourceType


def test_classify_manufacturer_marks_api_when_detected(db_session):
    m = manufacturer_crud.create_manufacturer(
        db_session, ManufacturerCreate(name="API OEM", website="https://api-oem.example")
    )

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/api/vehicles":
            return httpx.Response(200, json={}, headers={"content-type": "application/json"})
        return httpx.Response(404)

    client = httpx.Client(transport=httpx.MockTransport(handler))
    updated = dispatcher.classify_manufacturer(db_session, m, http_client=client)

    assert updated.data_source_type == DataSourceType.API
    assert updated.has_open_api is True
    assert updated.confidence_score == 0.7

    logs = db_session.query(m.__class__).count()  # sanity: manufacturer row still there
    assert logs == 1


def test_classify_manufacturer_marks_scraper_when_no_api(db_session):
    m = manufacturer_crud.create_manufacturer(
        db_session, ManufacturerCreate(name="No API OEM", website="https://no-api-oem.example")
    )

    client = httpx.Client(transport=httpx.MockTransport(lambda r: httpx.Response(404)))
    updated = dispatcher.classify_manufacturer(db_session, m, http_client=client)

    assert updated.data_source_type == DataSourceType.SCRAPER
    assert updated.has_open_api is False


def test_classify_pending_only_touches_unknown(db_session):
    manufacturer_crud.create_manufacturer(db_session, ManufacturerCreate(name="Unclassified OEM"))
    already_classified = manufacturer_crud.create_manufacturer(
        db_session, ManufacturerCreate(name="Already Classified", data_source_type="scraper")
    )

    results = dispatcher.classify_pending(db_session)

    names = [m.name for m in results]
    assert "Unclassified OEM" in names
    assert "Already Classified" not in names


def test_ingestion_persists_cars_and_variants_with_provenance(db_session):
    m = manufacturer_crud.create_manufacturer(
        db_session,
        ManufacturerCreate(
            name="Tata Motors",
            data_source_type="scraper",
            scraper_module="tests.fixtures.fake_scrapers.FakeTataScraper",
        ),
    )

    result = dispatcher.run_ingestion_for_manufacturer(db_session, m)

    assert result.cars_found == 1
    assert result.variants_found == 2
    assert result.variants_saved == 2
    assert result.errors == []

    from app.models.car import Car
    from app.models.variant import Variant

    car = db_session.query(Car).filter(Car.manufacturer_id == m.id).first()
    assert car.model == "Nexon"
    variants = db_session.query(Variant).filter(Variant.car_id == car.id).all()
    assert len(variants) == 2
    assert all(v.raw_source_url == "https://fake-tata.example/lineup" for v in variants)
    assert all(v.last_verified_at is not None for v in variants)


def test_ingestion_reruns_update_instead_of_duplicating(db_session):
    m = manufacturer_crud.create_manufacturer(
        db_session,
        ManufacturerCreate(
            name="Tata Motors",
            data_source_type="scraper",
            scraper_module="tests.fixtures.fake_scrapers.FakeTataScraper",
        ),
    )
    dispatcher.run_ingestion_for_manufacturer(db_session, m)
    dispatcher.run_ingestion_for_manufacturer(db_session, m)

    from app.models.car import Car

    cars = db_session.query(Car).filter(Car.manufacturer_id == m.id).all()
    assert len(cars) == 1  # not duplicated on second run


def test_ingestion_handles_scraper_failure_gracefully(db_session):
    m = manufacturer_crud.create_manufacturer(
        db_session,
        ManufacturerCreate(
            name="Broken OEM",
            data_source_type="scraper",
            scraper_module="tests.fixtures.fake_scrapers.FailingScraper",
        ),
    )
    result = dispatcher.run_ingestion_for_manufacturer(db_session, m)
    assert result.cars_found == 0
    assert len(result.errors) == 1
    assert "selectors" in result.errors[0]


def test_ingestion_without_scraper_module_fails_cleanly(db_session):
    m = manufacturer_crud.create_manufacturer(db_session, ManufacturerCreate(name="No Scraper OEM"))
    result = dispatcher.run_ingestion_for_manufacturer(db_session, m)
    assert result.errors == ["No scraper_module assigned to this manufacturer"]
