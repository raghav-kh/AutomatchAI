"""
Pipeline Step 4 (SRS Section 9): "Score vehicles".

Each factor is scored 0-10 independently (visible in ScoreBreakdown for
explainability -- SRS 4.4), then combined into a weighted total. Weights
shift based on what the user said mattered to them (safety_importance,
family_members, highway_usage, etc.) rather than being fixed, so two users
with the same shortlist of candidates can get different rankings.
"""

from dataclasses import dataclass

from app.models.variant import Variant
from app.schemas.preferences import UserPreferences, HighwayUsage, ParkingConstraint

# Component weight baseline -- tuned by preference signals in `_weights_for`.
BASE_WEIGHTS = {
    "budget_fit": 2.5,
    "safety": 1.5,
    "family_fit": 1.0,
    "city_comfort": 1.0,
    "highway_comfort": 1.0,
    "maintenance": 1.0,
    "resale_value": 0.7,
    "service_network": 1.0,
    "fuel_match": 1.0,
    "transmission_match": 0.5,
    "parking_fit": 1.0,
}


@dataclass
class ScoredComponents:
    budget_fit: float
    safety: float
    family_fit: float
    city_comfort: float
    highway_comfort: float
    maintenance: float
    resale_value: float
    service_network: float
    fuel_match: float
    transmission_match: float
    parking_fit: float

    def as_dict(self) -> dict[str, float]:
        return {
            "budget_fit": self.budget_fit,
            "safety": self.safety,
            "family_fit": self.family_fit,
            "city_comfort": self.city_comfort,
            "highway_comfort": self.highway_comfort,
            "maintenance": self.maintenance,
            "resale_value": self.resale_value,
            "service_network": self.service_network,
            "fuel_match": self.fuel_match,
            "transmission_match": self.transmission_match,
            "parking_fit": self.parking_fit,
        }


def _clamp(value: float, lo: float = 0.0, hi: float = 10.0) -> float:
    return max(lo, min(hi, value))


def _score_budget_fit(variant: Variant, prefs: UserPreferences) -> float:
    price = variant.price or 0
    if price <= prefs.budget:
        return 10.0
    overshoot_pct = (price - prefs.budget) / prefs.budget * 100
    return _clamp(10.0 - overshoot_pct * 2.5)  # steep penalty per % over budget


def _score_safety(variant: Variant) -> float:
    spec = variant.specifications
    if spec is None or spec.safety_rating is None:
        return 5.0  # neutral when unknown, not penalized for missing data
    return _clamp(spec.safety_rating * 2)  # 0-5 stars -> 0-10


def _score_family_fit(variant: Variant, prefs: UserPreferences) -> float:
    ai = variant.ai_attributes
    base = ai.family_score if ai and ai.family_score is not None else 5.0
    if prefs.family_members and prefs.family_members >= 5:
        spec = variant.specifications
        if spec and spec.seating and spec.seating < prefs.family_members:
            return _clamp(base - 4)  # can't actually seat the family -> heavy penalty
    if prefs.elderly_passengers and ai and ai.elderly_friendly is False:
        base -= 2
    elif prefs.elderly_passengers and ai and ai.elderly_friendly is True:
        base += 1
    return _clamp(base)


def _score_city_comfort(variant: Variant) -> float:
    ai = variant.ai_attributes
    return _clamp(ai.city_friendliness) if ai and ai.city_friendliness is not None else 5.0


def _score_highway_comfort(variant: Variant) -> float:
    ai = variant.ai_attributes
    return _clamp(ai.highway_comfort) if ai and ai.highway_comfort is not None else 5.0


def _score_maintenance(variant: Variant, prefs: UserPreferences) -> float:
    ai = variant.ai_attributes
    if ai is None or ai.maintenance_level is None:
        base = 5.0
    else:
        base = _clamp(10 - ai.maintenance_level)  # maintenance_level: lower = cheaper, so invert
    if prefs.beginner_driver and ai and ai.beginner_friendly:
        base += 1
    return _clamp(base)


def _score_resale(variant: Variant) -> float:
    ai = variant.ai_attributes
    return _clamp(ai.resale_value) if ai and ai.resale_value is not None else 5.0


def _score_service_network(variant: Variant) -> float:
    ai = variant.ai_attributes
    return _clamp(ai.service_network) if ai and ai.service_network is not None else 5.0


def _score_fuel_match(variant: Variant, prefs: UserPreferences) -> float:
    """
    Mirrors SRS 4.8 (Personalized Advice): short daily commutes make
    hybrid/EV less financially justified; frequent highway driving favors
    turbo petrol/diesel efficiency. If the user already filtered by fuel
    preference, this is a non-factor (already satisfied) -> neutral-high.
    """
    if prefs.fuel_preference:
        return 10.0  # hard-filtered already; nothing more to reward/penalize

    if prefs.daily_running_km is not None and prefs.daily_running_km < 20:
        if variant.fuel in ("Electric", "Hybrid"):
            return 4.0  # SRS 4.8: "Hybrid may not be financially beneficial" under 20km/day
    if prefs.highway_usage == HighwayUsage.FREQUENT and variant.fuel == "Petrol":
        return 7.0  # SRS 4.8 nudges toward turbo petrol/diesel for highway use
    return 8.0


def _score_transmission_match(variant: Variant, prefs: UserPreferences) -> float:
    if prefs.transmission_preference:
        return 10.0  # already hard-filtered
    return 8.0  # no preference stated -> neutral-high, don't penalize either way


def _score_parking_fit(variant: Variant, prefs: UserPreferences) -> float:
    spec = variant.specifications
    if spec is None or spec.length is None:
        return 5.0
    length = spec.length  # mm
    if prefs.parking_constraint == ParkingConstraint.TIGHT:
        # Favor shorter cars; ~3800mm hatchback baseline, penalize as length grows.
        return _clamp(10 - (length - 3800) / 60)
    if prefs.parking_constraint == ParkingConstraint.SPACIOUS:
        return 8.0  # parking space isn't a constraint, don't penalize larger cars
    return _clamp(10 - (length - 4200) / 150)  # normal: mild preference against very large cars


def _weights_for(prefs: UserPreferences) -> dict[str, float]:
    weights = dict(BASE_WEIGHTS)

    # safety_importance 1-5, 3 = neutral baseline
    weights["safety"] *= 1 + (prefs.safety_importance - 3) * 0.3

    if prefs.family_members and prefs.family_members >= 5:
        weights["family_fit"] *= 2.0
    elif not prefs.family_members:
        weights["family_fit"] *= 0.4

    if prefs.highway_usage == HighwayUsage.FREQUENT:
        weights["highway_comfort"] *= 2.0
        weights["city_comfort"] *= 0.6
    elif prefs.highway_usage == HighwayUsage.RARE:
        weights["city_comfort"] *= 1.5
        weights["highway_comfort"] *= 0.5

    weights["service_network"] *= 1 + (prefs.service_availability_importance - 3) * 0.3

    if prefs.parking_constraint == ParkingConstraint.TIGHT:
        weights["parking_fit"] *= 2.0

    return weights


def score_variant(variant: Variant, prefs: UserPreferences) -> tuple[ScoredComponents, float]:
    """Returns (component breakdown, weighted total on a 0-10 scale)."""
    components = ScoredComponents(
        budget_fit=_score_budget_fit(variant, prefs),
        safety=_score_safety(variant),
        family_fit=_score_family_fit(variant, prefs),
        city_comfort=_score_city_comfort(variant),
        highway_comfort=_score_highway_comfort(variant),
        maintenance=_score_maintenance(variant, prefs),
        resale_value=_score_resale(variant),
        service_network=_score_service_network(variant),
        fuel_match=_score_fuel_match(variant, prefs),
        transmission_match=_score_transmission_match(variant, prefs),
        parking_fit=_score_parking_fit(variant, prefs),
    )

    weights = _weights_for(prefs)
    values = components.as_dict()
    weighted_sum = sum(values[k] * weights[k] for k in values)
    total_weight = sum(weights.values())
    total = weighted_sum / total_weight if total_weight else 0.0

    return components, round(_clamp(total), 2)
