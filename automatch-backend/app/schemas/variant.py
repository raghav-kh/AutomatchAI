from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.specification import (
    SpecificationOut,
    SpecificationCreate,
    AIAttributesOut,
    AIAttributesCreate,
)


class VariantBase(BaseModel):
    variant_name: str
    price: float | None = None
    transmission: str | None = None
    fuel: str | None = None
    engine: str | None = None
    power: str | None = None
    torque: str | None = None
    mileage: float | None = None
    raw_source_url: str | None = None
    last_verified_at: datetime | None = None


class VariantCreate(VariantBase):
    specifications: SpecificationCreate | None = None
    ai_attributes: AIAttributesCreate | None = None


class VariantUpdate(BaseModel):
    variant_name: str | None = None
    price: float | None = None
    transmission: str | None = None
    fuel: str | None = None
    engine: str | None = None
    power: str | None = None
    torque: str | None = None
    mileage: float | None = None
    raw_source_url: str | None = None
    last_verified_at: datetime | None = None


class VariantOut(VariantBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    car_id: int
    specifications: SpecificationOut | None = None
    ai_attributes: AIAttributesOut | None = None
