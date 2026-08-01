from sqlalchemy.orm import Session, joinedload

from app.models.car import Car
from app.schemas.car import CarCreate, CarUpdate


def get_car(db: Session, car_id: int, with_variants: bool = False) -> Car | None:
    q = db.query(Car)
    if with_variants:
        q = q.options(joinedload(Car.variants))
    return q.filter(Car.id == car_id).first()


def list_cars(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    manufacturer_id: int | None = None,
    body_type: str | None = None,
) -> list[Car]:
    q = db.query(Car)
    if manufacturer_id is not None:
        q = q.filter(Car.manufacturer_id == manufacturer_id)
    if body_type is not None:
        q = q.filter(Car.body_type == body_type)
    return q.order_by(Car.model).offset(skip).limit(limit).all()


def create_car(db: Session, data: CarCreate) -> Car:
    obj = Car(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_car(db: Session, obj: Car, data: CarUpdate) -> Car:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete_car(db: Session, obj: Car) -> None:
    db.delete(obj)
    db.commit()
