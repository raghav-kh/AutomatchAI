from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.scrape_log import ScrapeStatus


class ScrapeLogCreate(BaseModel):
    source_type: str
    status: ScrapeStatus = ScrapeStatus.RUNNING
    records_found: int = 0
    records_saved: int = 0
    error_message: str | None = None


class ScrapeLogOut(ScrapeLogCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    manufacturer_id: int
    started_at: datetime
    finished_at: datetime | None = None
