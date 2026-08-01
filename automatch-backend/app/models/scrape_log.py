import enum
from datetime import datetime

from sqlalchemy import String, DateTime, Enum, ForeignKey, Integer, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ScrapeStatus(str, enum.Enum):
    SUCCESS = "success"
    FAILED = "failed"
    PARTIAL = "partial"
    RUNNING = "running"


class ScrapeLog(Base):
    """
    One row per pipeline run for a manufacturer. Lets us audit the
    'check API -> else scrape -> save under company' pipeline over time,
    and know which manufacturer/scraper needs attention when a site changes.
    """

    __tablename__ = "scrape_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    manufacturer_id: Mapped[int] = mapped_column(ForeignKey("manufacturers.id"), nullable=False)

    source_type: Mapped[str] = mapped_column(String(20), nullable=False)  # "api" | "scraper" | "manual"
    status: Mapped[ScrapeStatus] = mapped_column(Enum(ScrapeStatus), default=ScrapeStatus.RUNNING)
    records_found: Mapped[int] = mapped_column(Integer, default=0)
    records_saved: Mapped[int] = mapped_column(Integer, default=0)
    error_message: Mapped[str | None] = mapped_column(Text)

    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    manufacturer: Mapped["Manufacturer"] = relationship(back_populates="scrape_logs")
