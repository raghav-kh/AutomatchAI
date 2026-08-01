"""
Normalized shape that every data source (API client or scraper) must
produce, regardless of how it got the data. The dispatcher only knows how
to persist ScrapedCar/ScrapedVariant -- it never touches source-specific
parsing logic.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class ScrapedVariant:
    variant_name: str
    price: float | None = None
    transmission: str | None = None
    fuel: str | None = None
    engine: str | None = None
    power: str | None = None
    torque: str | None = None
    mileage: float | None = None

    # Provenance -- every scraped/fetched variant must say where it came from.
    source_url: str | None = None

    # Optional nested detail; left flat here since scrapers rarely get
    # crash-safety data cleanly. Populate via a follow-up enrichment pass.
    seating: int | None = None
    airbags: int | None = None
    safety_rating: float | None = None
    boot_space: float | None = None


@dataclass
class ScrapedCar:
    model: str
    body_type: str | None = None
    launch_year: int | None = None
    variants: list[ScrapedVariant] = field(default_factory=list)


@dataclass
class ProbeResult:
    """Result of checking whether a manufacturer exposes an open API."""

    has_api: bool
    endpoint: str | None = None
    confidence: float = 0.0
    notes: str | None = None


@dataclass
class IngestionResult:
    cars_found: int = 0
    variants_found: int = 0
    variants_saved: int = 0
    errors: list[str] = field(default_factory=list)
    fetched_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
