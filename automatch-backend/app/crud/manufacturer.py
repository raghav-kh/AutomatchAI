from sqlalchemy.orm import Session

from app.models.manufacturer import Manufacturer
from app.schemas.manufacturer import ManufacturerCreate, ManufacturerUpdate


def get_manufacturer(db: Session, manufacturer_id: int) -> Manufacturer | None:
    return db.get(Manufacturer, manufacturer_id)


def get_manufacturer_by_name(db: Session, name: str) -> Manufacturer | None:
    return db.query(Manufacturer).filter(Manufacturer.name == name).first()


def list_manufacturers(
    db: Session, skip: int = 0, limit: int = 100, only_active: bool = False
) -> list[Manufacturer]:
    q = db.query(Manufacturer)
    if only_active:
        q = q.filter(Manufacturer.is_active.is_(True))
    return q.order_by(Manufacturer.name).offset(skip).limit(limit).all()


def create_manufacturer(db: Session, data: ManufacturerCreate) -> Manufacturer:
    obj = Manufacturer(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_manufacturer(db: Session, obj: Manufacturer, data: ManufacturerUpdate) -> Manufacturer:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete_manufacturer(db: Session, obj: Manufacturer) -> None:
    db.delete(obj)
    db.commit()
