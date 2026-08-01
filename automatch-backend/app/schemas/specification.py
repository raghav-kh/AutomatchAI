from pydantic import BaseModel, ConfigDict


class SpecificationBase(BaseModel):
    seating: int | None = None
    airbags: int | None = None
    safety_rating: float | None = None
    ground_clearance: float | None = None
    boot_space: float | None = None
    wheelbase: float | None = None
    length: float | None = None
    width: float | None = None
    height: float | None = None


class SpecificationCreate(SpecificationBase):
    pass


class SpecificationUpdate(SpecificationBase):
    pass


class SpecificationOut(SpecificationBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    variant_id: int


class AIAttributesBase(BaseModel):
    ride_quality: float | None = None
    city_friendliness: float | None = None
    highway_comfort: float | None = None
    maintenance_level: float | None = None
    resale_value: float | None = None
    service_network: float | None = None
    beginner_friendly: bool | None = None
    family_score: float | None = None
    elderly_friendly: bool | None = None
    premium_feel: float | None = None
    offroad_capability: float | None = None


class AIAttributesCreate(AIAttributesBase):
    pass


class AIAttributesUpdate(AIAttributesBase):
    pass


class AIAttributesOut(AIAttributesBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    variant_id: int
