"""
Pipeline Steps 2-3 (SRS Section 9): "Convert to structured filters" and
"Query database". Deliberately loose on price (allows a bit over budget --
see 4.8 Personalized Advice / AI Budget Advisor idea) since the scoring
stage penalizes over-budget cars rather than hiding them outright; the
"increase budget by 1L -> better alternatives" feature needs those
candidates to exist in the pool.
"""

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_

from app.models.variant import Variant
from app.models.car import Car
from app.models.manufacturer import Manufacturer
from app.schemas.preferences import UserPreferences

BUDGET_OVERSHOOT_ALLOWANCE = 1.15  # allow candidates up to 15% over budget into the pool


def candidate_query(db: Session, prefs: UserPreferences):
    q = (
        db.query(Variant)
        .join(Car, Variant.car_id == Car.id)
        .join(Manufacturer, Car.manufacturer_id == Manufacturer.id)
        .options(
            joinedload(Variant.car).joinedload(Car.manufacturer),
            joinedload(Variant.specifications),
            joinedload(Variant.ai_attributes),
        )
        .filter(Manufacturer.is_active.is_(True))
        .filter(Variant.price.isnot(None))
        .filter(Variant.price <= prefs.budget * BUDGET_OVERSHOOT_ALLOWANCE)
    )

    if prefs.fuel_preference:
        q = q.filter(Variant.fuel == prefs.fuel_preference)

    if prefs.transmission_preference:
        q = q.filter(Variant.transmission == prefs.transmission_preference)

    if prefs.body_type_preference:
        q = q.filter(Car.body_type == prefs.body_type_preference)

    return q


def get_candidates(db: Session, prefs: UserPreferences, limit: int = 200) -> list[Variant]:
    return candidate_query(db, prefs).limit(limit).all()
