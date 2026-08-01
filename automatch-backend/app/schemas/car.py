from pydantic import BaseModel, ConfigDict

from app.schemas.variant import VariantOut


class CarBase(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    model: str
    body_type: str | None = None
    launch_year: int | None = None


class CarCreate(CarBase):
    manufacturer_id: int


class CarUpdate(BaseModel):
    model: str | None = None
    body_type: str | None = None
    launch_year: int | None = None


class CarOut(CarBase):
    model_config = ConfigDict(from_attributes=True, protected_namespaces=())
    id: int
    manufacturer_id: int


class CarWithVariantsOut(CarOut):
    variants: list[VariantOut] = []
