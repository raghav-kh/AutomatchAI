import enum
from datetime import datetime

from sqlalchemy import String, DateTime, Enum, Boolean, Float, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class DataSourceType(str, enum.Enum):
    """
    Drives the ingestion pipeline: for each manufacturer, we first check
    whether it exposes an open API. If yes -> API. If no -> a scraper module
    is assigned. UNKNOWN means nobody has investigated it yet.
    """

    API = "api"
    SCRAPER = "scraper"
    MANUAL = "manual"
    UNKNOWN = "unknown"


class Manufacturer(Base):
    __tablename__ = "manufacturers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    website: Mapped[str | None] = mapped_column(String(255))
    country: Mapped[str | None] = mapped_column(String(100))

    # --- Data sourcing pipeline metadata ---
    data_source_type: Mapped[DataSourceType] = mapped_column(
        Enum(DataSourceType), default=DataSourceType.UNKNOWN, nullable=False
    )
    has_open_api: Mapped[bool] = mapped_column(Boolean, default=False)
    api_endpoint: Mapped[str | None] = mapped_column(String(255))
    scraper_module: Mapped[str | None] = mapped_column(
        String(150), comment="Dotted path to the manufacturer-specific scraper, e.g. app.pipeline.scrapers.tata"
    )
    confidence_score: Mapped[float | None] = mapped_column(
        Float,
        comment="0-1 trust level in this manufacturer's data_source_type classification/data quality. "
        "API-sourced data should generally score higher than scraped data; feeds into AI scoring in Phase 2.",
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    last_updated: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())
    last_scraped_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    cars: Mapped[list["Car"]] = relationship(back_populates="manufacturer", cascade="all, delete-orphan")
    scrape_logs: Mapped[list["ScrapeLog"]] = relationship(back_populates="manufacturer", cascade="all, delete-orphan")
