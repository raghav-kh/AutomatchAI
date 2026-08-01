from sqlalchemy.orm import Session

from app.models.specification import Specification
from app.models.ai_attributes import AIAttributes
from app.schemas.specification import SpecificationUpdate, AIAttributesUpdate


def get_specification_by_variant(db: Session, variant_id: int) -> Specification | None:
    return db.query(Specification).filter(Specification.variant_id == variant_id).first()


def upsert_specification(db: Session, variant_id: int, data: SpecificationUpdate) -> Specification:
    obj = get_specification_by_variant(db, variant_id)
    if obj is None:
        obj = Specification(variant_id=variant_id, **data.model_dump(exclude_unset=True))
        db.add(obj)
    else:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj


def get_ai_attributes_by_variant(db: Session, variant_id: int) -> AIAttributes | None:
    return db.query(AIAttributes).filter(AIAttributes.variant_id == variant_id).first()


def upsert_ai_attributes(db: Session, variant_id: int, data: AIAttributesUpdate) -> AIAttributes:
    obj = get_ai_attributes_by_variant(db, variant_id)
    if obj is None:
        obj = AIAttributes(variant_id=variant_id, **data.model_dump(exclude_unset=True))
        db.add(obj)
    else:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj
