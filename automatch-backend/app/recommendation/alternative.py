"""
SRS 4.7 (Alternative Recommendation): "User selects Mahindra XUV 3XO ->
AI replies: You may also consider the Honda Elevate because: Better
refinement, Better resale, More reliable engine."

We look for variants in a similar price band and body type that clearly
outperform the reference on at least one AIAttributes dimension, and only
surface the reasons where the margin is meaningful -- no reason is shown
just to pad the list.
"""

from sqlalchemy.orm import Session, joinedload

from app.models.variant import Variant
from app.models.car import Car
from app.schemas.comparison import AlternativeSuggestion

PRICE_BAND_PCT = 0.20  # +/- 20% of the reference variant's price
MEANINGFUL_MARGIN = 1.0  # on a 0-10 AIAttributes scale
MAX_ALTERNATIVES = 3

# (ai_attributes field, higher_is_better, human-readable reason)
COMPARISON_DIMENSIONS = [
    ("premium_feel", True, "Better refinement"),
    ("resale_value", True, "Better resale value"),
    ("maintenance_level", False, "More reliable, lower maintenance"),  # lower maintenance_level = better
    ("highway_comfort", True, "More comfortable on highways"),
    ("city_friendliness", True, "Easier to live with in city traffic"),
    ("service_network", True, "Wider service network"),
]


def find_alternatives(db: Session, reference: Variant, limit: int = MAX_ALTERNATIVES) -> list[AlternativeSuggestion]:
    if not reference.price:
        return []

    low = reference.price * (1 - PRICE_BAND_PCT)
    high = reference.price * (1 + PRICE_BAND_PCT)

    candidates = (
        db.query(Variant)
        .join(Car, Variant.car_id == Car.id)
        .options(joinedload(Variant.car), joinedload(Variant.ai_attributes))
        .filter(Variant.id != reference.id)
        .filter(Variant.car_id != reference.car_id)  # a genuinely different model, not a trim sibling
        .filter(Variant.price.isnot(None))
        .filter(Variant.price.between(low, high))
        .all()
    )
    if reference.car and reference.car.body_type:
        candidates = [c for c in candidates if c.car and c.car.body_type == reference.car.body_type]

    ref_ai = reference.ai_attributes
    scored: list[tuple[Variant, list[str], float]] = []

    for candidate in candidates:
        cand_ai = candidate.ai_attributes
        if cand_ai is None:
            continue

        reasons: list[str] = []
        advantage = 0.0
        for field, higher_is_better, reason_text in COMPARISON_DIMENSIONS:
            cand_value = getattr(cand_ai, field, None)
            ref_value = getattr(ref_ai, field, None) if ref_ai else None
            if cand_value is None or ref_value is None:
                continue

            diff = (cand_value - ref_value) if higher_is_better else (ref_value - cand_value)
            if diff >= MEANINGFUL_MARGIN:
                reasons.append(reason_text)
                advantage += diff

        if reasons:
            scored.append((candidate, reasons, advantage))

    scored.sort(key=lambda t: t[2], reverse=True)

    return [
        AlternativeSuggestion(
            variant_id=candidate.id,
            car_model=candidate.car.model,
            variant_name=candidate.variant_name,
            manufacturer_name=candidate.car.manufacturer.name,
            reasons=reasons,
            price_difference=round((candidate.price or 0) - reference.price, 2),
        )
        for candidate, reasons, _ in scored[:limit]
    ]
