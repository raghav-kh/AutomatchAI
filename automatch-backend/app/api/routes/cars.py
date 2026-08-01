from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud import car as crud
from app.crud import manufacturer as manufacturer_crud
from app.models.user import User
from app.api.deps import require_admin
from app.schemas.car import CarCreate, CarUpdate, CarOut, CarWithVariantsOut

router = APIRouter(prefix="/cars", tags=["Cars"])


@router.post("", response_model=CarOut, status_code=201)
def create_car(payload: CarCreate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    if not manufacturer_crud.get_manufacturer(db, payload.manufacturer_id):
        raise HTTPException(status_code=404, detail="Manufacturer not found")
    return crud.create_car(db, payload)


@router.get("", response_model=list[CarOut])
def list_cars(
    skip: int = 0,
    limit: int = Query(default=100, le=500),
    manufacturer_id: int | None = None,
    body_type: str | None = None,
    db: Session = Depends(get_db),
):
    return crud.list_cars(db, skip=skip, limit=limit, manufacturer_id=manufacturer_id, body_type=body_type)


@router.get("/{car_id}", response_model=CarWithVariantsOut)
def get_car(car_id: int, db: Session = Depends(get_db)):
    obj = crud.get_car(db, car_id, with_variants=True)
    if not obj:
        raise HTTPException(status_code=404, detail="Car not found")
    return obj


@router.patch("/{car_id}", response_model=CarOut)
def update_car(car_id: int, payload: CarUpdate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    obj = crud.get_car(db, car_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Car not found")
    return crud.update_car(db, obj, payload)


@router.delete("/{car_id}", status_code=204)
def delete_car(car_id: int, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    obj = crud.get_car(db, car_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Car not found")
    crud.delete_car(db, obj)
