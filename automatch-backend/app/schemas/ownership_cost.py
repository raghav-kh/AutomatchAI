from pydantic import BaseModel, Field


class OwnershipCostInput(BaseModel):
    annual_km: float = Field(default=12000, gt=0, description="Expected annual driving distance in km")
    ownership_years: int = Field(default=5, ge=1, le=15)
    fuel_price_per_unit: float | None = Field(
        default=None,
        description="Override fuel price (INR/litre for Petrol/Diesel/CNG, INR/kWh for Electric). "
        "If omitted, a reasonable India-average default for the variant's fuel type is used.",
    )


class OwnershipCostBreakdown(BaseModel):
    purchase_price: float
    insurance_total: float
    fuel_total: float
    maintenance_total: float
    road_tax: float
    expected_resale_value: float
    total_ownership_cost: float
    net_cost_after_resale: float
    ownership_years: int
    annual_km: float
    assumptions: dict[str, float | str]
