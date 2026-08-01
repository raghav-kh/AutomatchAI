"""
SRS 4.5 (Ownership Cost Calculator): "Instead of showing only vehicle
price, calculate: Purchase Price, Insurance, Fuel, Maintenance, Road Tax,
Expected Resale, Estimated Five-Year Ownership Cost."

Every number here is a directional estimate built from India-average
defaults and the variant's own AIAttributes -- not a quote. The
`assumptions` dict on the response makes every input explicit so it can be
overridden or scrutinized, rather than presented as a hidden black box.
"""

from app.models.variant import Variant
from app.schemas.ownership_cost import OwnershipCostInput, OwnershipCostBreakdown

# India-average defaults, mid-2026 ballpark. Override via OwnershipCostInput.fuel_price_per_unit.
FUEL_PRICE_DEFAULTS = {"Petrol": 100.0, "Diesel": 92.0, "CNG": 75.0, "Electric": 8.0, "Hybrid": 100.0}
FUEL_PRICE_UNIT = {
    "Petrol": "INR/litre",
    "Diesel": "INR/litre",
    "CNG": "INR/kg",
    "Electric": "INR/kWh",
    "Hybrid": "INR/litre",
}
DEFAULT_MILEAGE_FALLBACK = {"Electric": 6.0}  # km per kWh, if not provided
DEFAULT_MILEAGE_GENERIC = 15.0  # kmpl fallback for petrol/diesel/CNG if not provided

ROAD_TAX_PCT_OF_PRICE = 0.10  # one-time; actual varies significantly by state
BASE_ANNUAL_MAINTENANCE = 8000.0  # INR/year at AIAttributes.maintenance_level == 5 (neutral)
FIRST_YEAR_INSURANCE_PCT = 0.035  # comprehensive premium as % of price, year 1
INSURANCE_YOY_DECLINE = 0.10  # premium roughly tracks declining IDV each year


def estimate_ownership_cost(variant: Variant, params: OwnershipCostInput) -> OwnershipCostBreakdown:
    price = variant.price or 0.0
    fuel_price = params.fuel_price_per_unit or FUEL_PRICE_DEFAULTS.get(variant.fuel, 100.0)
    mileage = variant.mileage or DEFAULT_MILEAGE_FALLBACK.get(variant.fuel, DEFAULT_MILEAGE_GENERIC)

    fuel_total = 0.0
    if mileage > 0:
        units_per_year = params.annual_km / mileage
        fuel_total = units_per_year * fuel_price * params.ownership_years

    ai = variant.ai_attributes
    maintenance_level = ai.maintenance_level if ai and ai.maintenance_level is not None else 5.0
    annual_maintenance = BASE_ANNUAL_MAINTENANCE * (maintenance_level / 5.0)
    maintenance_total = annual_maintenance * params.ownership_years

    insurance_total = 0.0
    premium = price * FIRST_YEAR_INSURANCE_PCT
    for _ in range(params.ownership_years):
        insurance_total += premium
        premium *= 1 - INSURANCE_YOY_DECLINE

    road_tax = price * ROAD_TAX_PCT_OF_PRICE

    resale_score = ai.resale_value if ai and ai.resale_value is not None else 5.0
    base_depreciation_retention = max(0.25, 1 - 0.13 * params.ownership_years)
    resale_adjustment = 0.7 + (resale_score / 10) * 0.6  # AIAttributes.resale_value scales 0.7x-1.3x
    retention = min(0.9, base_depreciation_retention * resale_adjustment)
    expected_resale_value = price * retention

    total_ownership_cost = price + insurance_total + fuel_total + maintenance_total + road_tax
    net_cost_after_resale = total_ownership_cost - expected_resale_value

    return OwnershipCostBreakdown(
        purchase_price=round(price, 2),
        insurance_total=round(insurance_total, 2),
        fuel_total=round(fuel_total, 2),
        maintenance_total=round(maintenance_total, 2),
        road_tax=round(road_tax, 2),
        expected_resale_value=round(expected_resale_value, 2),
        total_ownership_cost=round(total_ownership_cost, 2),
        net_cost_after_resale=round(net_cost_after_resale, 2),
        ownership_years=params.ownership_years,
        annual_km=params.annual_km,
        assumptions={
            "fuel_price_per_unit": fuel_price,
            "fuel_price_unit": FUEL_PRICE_UNIT.get(variant.fuel, "INR/litre"),
            "mileage_used": mileage,
            "road_tax_pct_of_price": ROAD_TAX_PCT_OF_PRICE,
            "first_year_insurance_pct": FIRST_YEAR_INSURANCE_PCT,
            "insurance_yoy_decline_pct": INSURANCE_YOY_DECLINE,
            "note": "Estimates only -- actual insurance, road tax, and resale vary by state, insurer, and market.",
        },
    )
