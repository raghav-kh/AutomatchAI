"""
Orchestrates the two pipeline stages described in the SRS:

1. classify_pending(): for every manufacturer with data_source_type=UNKNOWN,
   probe for an open API; if found, mark data_source_type=API; if not,
   mark data_source_type=SCRAPER. Either way, a human/future step still
   needs to assign scraper_module (and, for API manufacturers, confirm
   api_endpoint) -- classification only decides *which kind* of sourcing
   this manufacturer needs.

2. run_ingestion_for_manufacturer(): given a manufacturer with
   scraper_module assigned, fetch its current lineup and persist
   Car/Variant/Specification rows with provenance. Works uniformly for
   both HTML scrapers (BaseScraper) and JSON API clients (BaseApiClient,
   e.g. scrapers/nhtsa_vpic.py) -- see _instantiate_ingestion_source.

Both stages always write a ScrapeLog row so every run is auditable.
"""

import importlib
from datetime import datetime, timezone

import httpx
from sqlalchemy.orm import Session

from app.models.manufacturer import Manufacturer, DataSourceType
from app.models.scrape_log import ScrapeStatus
from app.models.car import Car
from app.models.variant import Variant
from app.pipeline.api_probe import probe_manufacturer_api
from app.pipeline.schemas import ScrapedCar, IngestionResult
from app.pipeline.scrapers.base import BaseScraper, BaseApiClient, ScraperImportError
from app.crud import scrape_log as scrape_log_crud
from app.schemas.scrape_log import ScrapeLogCreate


# ---------------------------------------------------------------------------
# Stage 1: classification
# ---------------------------------------------------------------------------

def classify_manufacturer(db: Session, manufacturer: Manufacturer, http_client: httpx.Client | None = None) -> Manufacturer:
    """Probe one manufacturer and update its data_source_type/confidence_score."""
    result = probe_manufacturer_api(manufacturer.website, client=http_client)

    if result.has_api:
        manufacturer.data_source_type = DataSourceType.API
        manufacturer.has_open_api = True
        manufacturer.api_endpoint = result.endpoint
    else:
        manufacturer.data_source_type = DataSourceType.SCRAPER
        manufacturer.has_open_api = False

    manufacturer.confidence_score = result.confidence
    db.add(manufacturer)

    scrape_log_crud.create_log(
        db,
        manufacturer.id,
        ScrapeLogCreate(
            source_type=manufacturer.data_source_type.value,
            status=ScrapeStatus.SUCCESS,
            records_found=0,
            records_saved=0,
            error_message=result.notes,
        ),
    )

    db.commit()
    db.refresh(manufacturer)
    return manufacturer


def classify_pending(db: Session, limit: int | None = None) -> list[Manufacturer]:
    """Run classify_manufacturer() over every UNKNOWN manufacturer, once."""
    query = db.query(Manufacturer).filter(Manufacturer.data_source_type == DataSourceType.UNKNOWN)
    if limit:
        query = query.limit(limit)
    pending = query.all()

    # Share one httpx.Client across the batch for connection reuse.
    with httpx.Client(timeout=5.0, follow_redirects=True) as client:
        for m in pending:
            classify_manufacturer(db, m, http_client=client)

    return pending


# ---------------------------------------------------------------------------
# Stage 2: ingestion
# ---------------------------------------------------------------------------

def _load_ingestion_class(dotted_path: str) -> type[BaseScraper]:
    """dotted_path like 'app.pipeline.scrapers.tata.TataScraper'."""
    module_path, _, class_name = dotted_path.rpartition(".")
    if not module_path:
        raise ScraperImportError(f"Invalid scraper_module path: {dotted_path!r}")
    try:
        module = importlib.import_module(module_path)
        cls = getattr(module, class_name)
    except (ImportError, AttributeError) as exc:
        raise ScraperImportError(f"Could not load scraper {dotted_path!r}: {exc}") from exc

    if not (isinstance(cls, type) and issubclass(cls, BaseScraper)):
        raise ScraperImportError(f"{dotted_path!r} is not a BaseScraper/BaseApiClient subclass")
    return cls


def _instantiate_ingestion_source(manufacturer: Manufacturer) -> BaseScraper:
    """
    Instantiates manufacturer.scraper_module correctly for either shape:
    - BaseApiClient subclasses need the endpoint (discovered per-manufacturer
      at classification time or set manually), so they take it at construction.
    - Plain BaseScraper subclasses (HTML scrapers) hardcode their own target
      URL(s) as a class attribute, so they take no constructor args.
    Dispatch is based on the actual class, not manufacturer.data_source_type,
    so a class always behaves the same way regardless of how the DB row
    happens to be classified.
    """
    cls = _load_ingestion_class(manufacturer.scraper_module)

    if issubclass(cls, BaseApiClient):
        if not manufacturer.api_endpoint:
            raise ScraperImportError(
                f"{manufacturer.scraper_module!r} is a BaseApiClient but "
                f"manufacturer {manufacturer.name!r} has no api_endpoint set"
            )
        return cls(api_endpoint=manufacturer.api_endpoint)

    return cls()


def _persist_scraped_cars(db: Session, manufacturer: Manufacturer, cars: list[ScrapedCar]) -> IngestionResult:
    result = IngestionResult(cars_found=len(cars))
    now = datetime.now(timezone.utc)

    for scraped_car in cars:
        car = (
            db.query(Car)
            .filter(Car.manufacturer_id == manufacturer.id, Car.model == scraped_car.model)
            .first()
        )
        if car is None:
            car = Car(
                manufacturer_id=manufacturer.id,
                model=scraped_car.model,
                body_type=scraped_car.body_type,
                launch_year=scraped_car.launch_year,
            )
            db.add(car)
            db.flush()

        for sv in scraped_car.variants:
            result.variants_found += 1
            variant = (
                db.query(Variant)
                .filter(Variant.car_id == car.id, Variant.variant_name == sv.variant_name)
                .first()
            )
            if variant is None:
                variant = Variant(car_id=car.id, variant_name=sv.variant_name)
                db.add(variant)

            variant.price = sv.price
            variant.transmission = sv.transmission
            variant.fuel = sv.fuel
            variant.engine = sv.engine
            variant.power = sv.power
            variant.torque = sv.torque
            variant.mileage = sv.mileage
            variant.raw_source_url = sv.source_url
            variant.last_verified_at = now

            result.variants_saved += 1

    manufacturer.last_scraped_at = now
    db.add(manufacturer)
    db.commit()
    return result


def run_ingestion_for_manufacturer(db: Session, manufacturer: Manufacturer) -> IngestionResult:
    """
    Fetch this manufacturer's current lineup via its assigned ingestion
    source (a BaseScraper for HTML scraping, or a BaseApiClient for a
    JSON API -- see _instantiate_ingestion_source) and persist it. Always
    logs a ScrapeLog, success or fail.
    """
    if not manufacturer.scraper_module:
        result = IngestionResult(errors=["No scraper_module assigned to this manufacturer"])
        scrape_log_crud.create_log(
            db,
            manufacturer.id,
            ScrapeLogCreate(
                source_type=manufacturer.data_source_type.value,
                status=ScrapeStatus.FAILED,
                error_message=result.errors[0],
            ),
        )
        return result

    try:
        source = _instantiate_ingestion_source(manufacturer)
        scraped_cars = source.scrape()
        result = _persist_scraped_cars(db, manufacturer, scraped_cars)
        status = ScrapeStatus.SUCCESS if not result.errors else ScrapeStatus.PARTIAL
    except Exception as exc:  # noqa: BLE001 - a single bad manufacturer must not crash the batch
        result = IngestionResult(errors=[str(exc)])
        status = ScrapeStatus.FAILED

    scrape_log_crud.create_log(
        db,
        manufacturer.id,
        ScrapeLogCreate(
            source_type=manufacturer.data_source_type.value,
            status=status,
            records_found=result.cars_found,
            records_saved=result.variants_saved,
            error_message="; ".join(result.errors) if result.errors else None,
        ),
    )
    return result
