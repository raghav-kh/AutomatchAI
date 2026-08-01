"""
SRS 4.6 (Smart Comparisons): compare multiple vehicles side by side across
performance, safety, features, maintenance, boot space, ground clearance,
rear seat comfort, and AI recommendation score.

"AI recommendation score" here uses neutral preferences (budget set to
each variant's own price, so budget fit never penalizes it) -- this is a
context-free quality score, distinct from the personalized score used in
/recommendations, which depends on what a specific buyer said they wanted.
"""

from sqlalchemy.orm import Session, joinedload

from app.models.variant import Variant
from app.schemas.preferences import UserPreferences
from app.schemas.comparison import ComparisonRow
from app.recommendation.scoring import score_variant


def _neutral_score(variant: Variant) -> float:
    prefs = UserPreferences(budget=variant.price or 1)  # budget=own price -> budget_fit never penalizes
    _, total = score_variant(variant, prefs)
    return total


def compare_variants(db: Session, variant_ids: list[int]) -> list[ComparisonRow]:
    """Returns comparison rows in the same order as `variant_ids`. Raises ValueError if any id is missing."""
    variants = (
        db.query(Variant)
        .options(
            joinedload(Variant.car),
            joinedload(Variant.specifications),
            joinedload(Variant.ai_attributes),
        )
        .filter(Variant.id.in_(variant_ids))
        .all()
    )
    by_id = {v.id: v for v in variants}

    missing = [vid for vid in variant_ids if vid not in by_id]
    if missing:
        raise ValueError(f"Variant ids not found: {missing}")

    rows = []
    for vid in variant_ids:
        v = by_id[vid]
        spec = v.specifications
        ai = v.ai_attributes
        rows.append(
            ComparisonRow(
                variant_id=v.id,
                car_model=v.car.model,
                variant_name=v.variant_name,
                manufacturer_name=v.car.manufacturer.name,
                price=v.price,
                power=v.power,
                torque=v.torque,
                mileage=v.mileage,
                safety_rating=spec.safety_rating if spec else None,
                airbags=spec.airbags if spec else None,
                maintenance_level=ai.maintenance_level if ai else None,
                boot_space=spec.boot_space if spec else None,
                ground_clearance=spec.ground_clearance if spec else None,
                family_score=ai.family_score if ai else None,
                ai_recommendation_score=_neutral_score(v),
            )
        )
    return rows
