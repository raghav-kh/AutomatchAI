from app.models.variant import Variant
from app.models.ai_attributes import AIAttributes
from app.schemas.ownership_cost import OwnershipCostInput
from app.recommendation.ownership_cost import estimate_ownership_cost


def make_variant(price=1000000, fuel="Petrol", mileage=18.0, ai_attributes=None) -> Variant:
    v = Variant(id=1, car_id=1, variant_name="Test", price=price, fuel=fuel, mileage=mileage)
    v.ai_attributes = ai_attributes
    return v


def test_total_cost_includes_all_components():
    v = make_variant()
    result = estimate_ownership_cost(v, OwnershipCostInput())
    assert result.purchase_price == 1000000.0
    assert result.insurance_total > 0
    assert result.fuel_total > 0
    assert result.maintenance_total > 0
    assert result.road_tax > 0
    assert result.expected_resale_value > 0
    assert result.total_ownership_cost == round(
        result.purchase_price + result.insurance_total + result.fuel_total + result.maintenance_total + result.road_tax,
        2,
    )
    assert result.net_cost_after_resale == round(result.total_ownership_cost - result.expected_resale_value, 2)


def test_higher_maintenance_level_increases_maintenance_cost():
    low_maint = make_variant(ai_attributes=AIAttributes(maintenance_level=2))
    high_maint = make_variant(ai_attributes=AIAttributes(maintenance_level=9))

    low_result = estimate_ownership_cost(low_maint, OwnershipCostInput())
    high_result = estimate_ownership_cost(high_maint, OwnershipCostInput())
    assert high_result.maintenance_total > low_result.maintenance_total


def test_higher_resale_score_increases_expected_resale_value():
    low_resale = make_variant(ai_attributes=AIAttributes(resale_value=2))
    high_resale = make_variant(ai_attributes=AIAttributes(resale_value=9))

    low_result = estimate_ownership_cost(low_resale, OwnershipCostInput())
    high_result = estimate_ownership_cost(high_resale, OwnershipCostInput())
    assert high_result.expected_resale_value > low_result.expected_resale_value


def test_more_annual_km_increases_fuel_cost():
    v = make_variant()
    low_km = estimate_ownership_cost(v, OwnershipCostInput(annual_km=5000))
    high_km = estimate_ownership_cost(v, OwnershipCostInput(annual_km=25000))
    assert high_km.fuel_total > low_km.fuel_total


def test_electric_uses_kwh_pricing_and_fallback_efficiency():
    v = make_variant(fuel="Electric", mileage=None)
    result = estimate_ownership_cost(v, OwnershipCostInput())
    assert result.assumptions["fuel_price_unit"] == "INR/kWh"
    assert result.assumptions["mileage_used"] == 6.0  # fallback km/kWh
    assert result.fuel_total > 0


def test_custom_fuel_price_override_is_respected():
    v = make_variant()
    default_result = estimate_ownership_cost(v, OwnershipCostInput())
    overridden = estimate_ownership_cost(v, OwnershipCostInput(fuel_price_per_unit=150.0))
    assert overridden.fuel_total > default_result.fuel_total
    assert overridden.assumptions["fuel_price_per_unit"] == 150.0


def test_missing_ai_attributes_uses_neutral_defaults():
    v = make_variant(ai_attributes=None)
    result = estimate_ownership_cost(v, OwnershipCostInput())
    assert result.maintenance_total > 0
    assert result.expected_resale_value > 0
