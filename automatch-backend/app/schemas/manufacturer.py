from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.manufacturer import DataSourceType


class ManufacturerBase(BaseModel):
    name: str
    website: str | None = None
    country: str | None = None
    data_source_type: DataSourceType = DataSourceType.UNKNOWN
    has_open_api: bool = False
    api_endpoint: str | None = None
    scraper_module: str | None = None
    confidence_score: float | None = Field(default=None, ge=0, le=1)
    is_active: bool = True


class ManufacturerCreate(ManufacturerBase):
    pass


class ManufacturerUpdate(BaseModel):
    name: str | None = None
    website: str | None = None
    country: str | None = None
    data_source_type: DataSourceType | None = None
    has_open_api: bool | None = None
    api_endpoint: str | None = None
    scraper_module: str | None = None
    confidence_score: float | None = Field(default=None, ge=0, le=1)
    is_active: bool | None = None


class ManufacturerOut(ManufacturerBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    last_updated: datetime | None = None
    last_scraped_at: datetime | None = None
    created_at: datetime
