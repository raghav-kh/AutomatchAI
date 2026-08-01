from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.models.variant import Variant
from app.models.specification import Specification
from app.models.ai_attributes import AIAttributes
from app.schemas.variant import VariantCreate, VariantUpdate


def get_variant(db: Session, variant_id: int) -> Variant | None:
    return db.get(Variant, variant_id)


def list_variants(db: Session, skip: int = 0, limit: int = 100, car_id: int | None = None) -> list[Variant]:
    q = db.query(Variant)
    if car_id is not None:
        q = q.filter(Variant.car_id == car_id)
    return q.offset(skip).limit(limit).all()


def create_variant(db: Session, car_id: int, data: VariantCreate) -> Variant:
    payload = data.model_dump(exclude={"specifications", "ai_attributes"})
    obj = Variant(car_id=car_id, **payload)
    db.add(obj)
    db.flush()  # get obj.id before attaching children

    if data.specifications is not None:
        db.add(Specification(variant_id=obj.id, **data.specifications.model_dump()))
    if data.ai_attributes is not None:
        db.add(AIAttributes(variant_id=obj.id, **data.ai_attributes.model_dump()))

    db.commit()
    db.refresh(obj)
    return obj


def update_variant(db: Session, obj: Variant, data: VariantUpdate) -> Variant:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete_variant(db: Session, obj: Variant) -> None:
    db.delete(obj)
    db.commit()


def list_stale_variants(db: Session, days: int = 90) -> list[Variant]:
    """
    Variants either never verified, or not verified within `days`.
    Feeds a future 're-check this manufacturer' pipeline job -- a variant
    whose raw_source_url hasn't been re-confirmed recently may have a
    stale price or spec.
    """
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    return (
        db.query(Variant)
        .filter((Variant.last_verified_at.is_(None)) | (Variant.last_verified_at < cutoff))
        .all()
    )
