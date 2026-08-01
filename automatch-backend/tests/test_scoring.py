from app.models.variant import Variant
from app.models.car import Car
from app.models.manufacturer import Manufacturer
from app.models.specification import Specification
from app.models.ai_attributes import AIAttributes
from app.schemas.preferences import UserPreferences, HighwayUsage, ParkingConstraint
from app.recommendation.scoring import score_variant, _score_budget_fit, _score_parking_fit


def make_variant(**kwargs) -> Variant:
    manufacturer = Manufacturer(id=1, name="Test OEM")
    car = Car(id=1, manufacturer_id=1, model="Test Car", body_type="SUV")
    car.manufacturer = manufacturer
    variant = Variant(
        id=1,
        car_id=1,
        variant_name="Base",
        price=kwargs.get("price", 1000000),
        fuel=kwargs.get("fuel", "Petrol"),
        transmission=kwargs.get("transmission", "Manual"),
        mileage=kwargs.get("mileage", 18.0),
    )
    variant.car = car
    variant.specifications = kwargs.get("specifications")
    variant.ai_attributes = kwargs.get("ai_attributes")
    return variant


def test_budget_fit_within_budget_is_perfect():
    v = make_variant(price=900000)
    prefs = UserPreferences(budget=1000000)
    assert _score_budget_fit(v, prefs) == 10.0


def test_budget_fit_penalizes_overshoot():
    v = make_variant(price=1200000)
    prefs = UserPreferences(budget=1000000)
    score = _score_budget_fit(v, prefs)
    assert score < 10.0
    assert score >= 0.0


def test_budget_fit_zero_far_over_budget():
    v = make_variant(price=2000000)
    prefs = UserPreferences(budget=1000000)
    assert _score_budget_fit(v, prefs) == 0.0


def test_family_fit_penalizes_insufficient_seating():
    spec = Specification(seating=5)
    ai = AIAttributes(family_score=8.0)
    v = make_variant(specifications=spec, ai_attributes=ai)
    prefs = UserPreferences(budget=1000000, family_members=7)
    components, _ = score_variant(v, prefs)
    assert components.family_fit < 8.0


def test_family_fit_no_penalty_when_seating_sufficient():
    spec = Specification(seating=7)
    ai = AIAttributes(family_score=8.0)
    v = make_variant(specifications=spec, ai_attributes=ai)
    prefs = UserPreferences(budget=1000000, family_members=7)
    components, _ = score_variant(v, prefs)
    assert components.family_fit == 8.0


def test_fuel_match_penalizes_ev_for_short_commute():
    v = make_variant(fuel="Electric")
    prefs = UserPreferences(budget=1000000, daily_running_km=10)
    components, _ = score_variant(v, prefs)
    assert components.fuel_match == 4.0


def test_fuel_match_neutral_when_fuel_preference_set():
    v = make_variant(fuel="Electric")
    prefs = UserPreferences(budget=1000000, daily_running_km=10, fuel_preference="Electric")
    components, _ = score_variant(v, prefs)
    assert components.fuel_match == 10.0


def test_parking_fit_favors_shorter_cars_when_tight():
    short_spec = Specification(length=3800)
    long_spec = Specification(length=4600)
    prefs = UserPreferences(budget=1000000, parking_constraint=ParkingConstraint.TIGHT)

    short_score = _score_parking_fit(make_variant(specifications=short_spec), prefs)
    long_score = _score_parking_fit(make_variant(specifications=long_spec), prefs)
    assert short_score > long_score


def test_highway_frequent_shifts_weight_toward_highway_comfort():
    ai_highway_strong = AIAttributes(highway_comfort=9.0, city_friendliness=3.0)
    v = make_variant(ai_attributes=ai_highway_strong)
    prefs_highway = UserPreferences(budget=1000000, highway_usage=HighwayUsage.FREQUENT)
    prefs_city = UserPreferences(budget=1000000, highway_usage=HighwayUsage.RARE)

    _, total_highway_pref = score_variant(v, prefs_highway)
    _, total_city_pref = score_variant(v, prefs_city)
    # Same car (strong highway, weak city) should score higher when user prioritizes highway use
    assert total_highway_pref > total_city_pref


def test_missing_data_defaults_to_neutral_not_zero():
    v = make_variant()  # no specifications, no ai_attributes
    prefs = UserPreferences(budget=1000000)
    components, total = score_variant(v, prefs)
    assert components.safety == 5.0
    assert components.family_fit == 5.0
    assert total > 0
