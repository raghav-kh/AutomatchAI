from enum import Enum

from pydantic import BaseModel, Field


class HighwayUsage(str, Enum):
    RARE = "rare"
    OCCASIONAL = "occasional"
    FREQUENT = "frequent"


class ParkingConstraint(str, Enum):
    TIGHT = "tight"  # narrow street / small society parking -> favor compact cars
    NORMAL = "normal"
    SPACIOUS = "spacious"


class UserPreferences(BaseModel):
    """
    Structured form of what Section 4.1 (AI Preference Collection) of the
    SRS calls "natural questions". A future conversational layer can map
    free-text answers into this shape before calling /recommendations --
    this model is the "structured search criteria" the SRS describes.
    """

    budget: float = Field(..., gt=0, description="Max ex-showroom budget in INR")
    city: str | None = None
    family_members: int | None = Field(default=None, ge=1, le=10)
    daily_running_km: float | None = Field(default=None, ge=0)
    highway_usage: HighwayUsage = HighwayUsage.OCCASIONAL
    fuel_preference: str | None = None  # "Petrol" | "Diesel" | "CNG" | "Electric" | "Hybrid" | None = no preference
    transmission_preference: str | None = None  # "Manual" | "Automatic" | None = no preference
    body_type_preference: str | None = None  # e.g. "SUV"; None = no filter
    service_availability_importance: int = Field(default=3, ge=1, le=5)
    safety_importance: int = Field(default=3, ge=1, le=5)
    parking_constraint: ParkingConstraint = ParkingConstraint.NORMAL
    elderly_passengers: bool = False
    beginner_driver: bool = False
