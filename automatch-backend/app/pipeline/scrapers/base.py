"""
Every manufacturer-specific scraper lives in app/pipeline/scrapers/ and
subclasses BaseScraper. The dispatcher looks up the class by the dotted
path stored in Manufacturer.scraper_module and calls .scrape().

Design intent: "only the affected manufacturer's scraper needs updating
if a website changes" (per the SRS) -- each scraper is fully self-contained
and knows nothing about the DB, the dispatcher, or other manufacturers.
"""

from abc import ABC, abstractmethod

from app.pipeline.schemas import ScrapedCar


class BaseScraper(ABC):
    #: Human-readable manufacturer name, must match Manufacturer.name in the DB.
    manufacturer_name: str = "Unknown"

    #: Base URL this scraper targets, used for logging/debugging only.
    base_url: str = ""

    @abstractmethod
    def scrape(self) -> list[ScrapedCar]:
        """
        Fetch and parse this manufacturer's current lineup.
        Must return normalized ScrapedCar/ScrapedVariant objects with
        `source_url` populated on every variant. Raise on hard failure --
        the dispatcher will catch it and log a `failed` ScrapeLog.
        """
        raise NotImplementedError


class ScraperImportError(Exception):
    """Raised when Manufacturer.scraper_module doesn't resolve to a valid BaseScraper subclass."""


class BaseApiClient(BaseScraper):
    """
    For manufacturers classified data_source_type=api. Same output
    contract as BaseScraper (scrape() -> list[ScrapedCar]), but the
    endpoint isn't a hardcoded class attribute like a scraper's base_url --
    it's whatever Manufacturer.api_endpoint holds, discovered by the
    classification probe or set manually by an admin. So this takes the
    endpoint at construction time instead.

    The dispatcher detects which constructor shape to use by checking
    `issubclass(cls, BaseApiClient)` before instantiating -- see
    app/pipeline/dispatcher.py::_load_ingestion_class.
    """

    def __init__(self, api_endpoint: str):
        self.api_endpoint = api_endpoint
