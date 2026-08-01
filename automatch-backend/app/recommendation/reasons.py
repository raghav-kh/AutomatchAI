"""
Turns the numeric ScoredComponents into the human-readable bullet lists
the SRS examples show ("Recommended because: Fits your budget / Excellent
rear seat comfort..." and "Trade-offs: Smaller service network / Average
resale value"). This is template-based and needs no LLM call -- it always
runs, even if Groq isn't configured.
"""

from app.recommendation.scoring import ScoredComponents
from app.schemas.preferences import UserPreferences

STRONG_THRESHOLD = 8.0
WEAK_THRESHOLD = 4.5

POSITIVE_TEMPLATES = {
    "budget_fit": "Fits comfortably within your budget",
    "safety": "Strong safety rating",
    "family_fit": "Great fit for a larger family",
    "city_comfort": "Easy to drive and park in city traffic",
    "highway_comfort": "Suitable for long highway trips",
    "maintenance": "Low running/maintenance cost",
    "resale_value": "Holds resale value well",
    "service_network": "Wide service network availability",
    "fuel_match": "Fuel choice suits your driving pattern",
    "transmission_match": "Transmission matches your preference",
    "parking_fit": "Compact and easy to park",
}

TRADE_OFF_TEMPLATES = {
    "budget_fit": "Priced above your stated budget",
    "safety": "Below-average safety rating for this segment",
    "family_fit": "Not ideally suited for a large family",
    "city_comfort": "Less nimble in dense city traffic",
    "highway_comfort": "Less composed on long highway drives",
    "maintenance": "Higher running/maintenance cost than average",
    "resale_value": "Average-to-below-average resale value",
    "service_network": "Smaller service network in some regions",
    "fuel_match": "Fuel type may not suit your driving pattern",
    "transmission_match": "Transmission may not match your preference",
    "parking_fit": "Larger footprint, may be harder to park",
}

EXTRA_POSITIVE_TEMPLATES = {
    "elderly_passengers": "Comfortable rear seat access for elderly passengers",
    "beginner_driver": "Easy to drive for a beginner",
}


TRADE_OFF_TO_COMPONENT = {v: k for k, v in TRADE_OFF_TEMPLATES.items()}


def trade_off_component_keys(trade_offs: list[str]) -> list[str]:
    """Maps display trade-off text back to the scoring component key that produced it."""
    return [TRADE_OFF_TO_COMPONENT[t] for t in trade_offs if t in TRADE_OFF_TO_COMPONENT]


def build_reasons_and_tradeoffs(
    components: ScoredComponents, prefs: UserPreferences
) -> tuple[list[str], list[str]]:
    values = components.as_dict()

    reasons = [POSITIVE_TEMPLATES[k] for k, v in values.items() if v >= STRONG_THRESHOLD]
    trade_offs = [TRADE_OFF_TEMPLATES[k] for k, v in values.items() if v <= WEAK_THRESHOLD]

    if prefs.elderly_passengers and values["family_fit"] >= STRONG_THRESHOLD:
        reasons.append(EXTRA_POSITIVE_TEMPLATES["elderly_passengers"])
    if prefs.beginner_driver and values["maintenance"] >= STRONG_THRESHOLD:
        reasons.append(EXTRA_POSITIVE_TEMPLATES["beginner_driver"])

    # Every recommendation should say *something* positive, even a modest match.
    if not reasons:
        best_key = max(values, key=values.get)
        reasons.append(POSITIVE_TEMPLATES[best_key])

    return reasons, trade_offs
