from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud import variant as crud
from app.crud import car as car_crud
from app.crud import specification as spec_crud
from app.schemas.variant import VariantCreate, VariantUpdate, VariantOut
from app.schemas.specification import SpecificationUpdate, SpecificationOut, AIAttributesUpdate, AIAttributesOut
from app.schemas.ownership_cost import OwnershipCostInput, OwnershipCostBreakdown
from app.recommendation.ownership_cost import estimate_ownership_cost
from app.models.user import User
from app.api.deps import require_admin

router = APIRouter(tags=["Variants"])


@router.get("/variants/stale", response_model=list[VariantOut])
def list_stale_variants(days: int = Query(default=90, ge=1), db: Session = Depends(get_db)):
    """Variants not re-verified against their source in the last `days` days."""
    return crud.list_stale_variants(db, days=days)


@router.post("/cars/{car_id}/variants", response_model=VariantOut, status_code=201)
def create_variant(car_id: int, payload: VariantCreate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    if not car_crud.get_car(db, car_id):
        raise HTTPException(status_code=404, detail="Car not found")
    return crud.create_variant(db, car_id, payload)


@router.get("/cars/{car_id}/variants", response_model=list[VariantOut])
def list_variants_for_car(car_id: int, skip: int = 0, limit: int = Query(default=100, le=500), db: Session = Depends(get_db)):
    return crud.list_variants(db, skip=skip, limit=limit, car_id=car_id)


@router.get("/variants/{variant_id}", response_model=VariantOut)
def get_variant(variant_id: int, db: Session = Depends(get_db)):
    obj = crud.get_variant(db, variant_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Variant not found")
    return obj


@router.patch("/variants/{variant_id}", response_model=VariantOut)
def update_variant(variant_id: int, payload: VariantUpdate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    obj = crud.get_variant(db, variant_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Variant not found")
    return crud.update_variant(db, obj, payload)


@router.delete("/variants/{variant_id}", status_code=204)
def delete_variant(variant_id: int, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    obj = crud.get_variant(db, variant_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Variant not found")
    crud.delete_variant(db, obj)


@router.put("/variants/{variant_id}/specifications", response_model=SpecificationOut)
def upsert_specifications(variant_id: int, payload: SpecificationUpdate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    if not crud.get_variant(db, variant_id):
        raise HTTPException(status_code=404, detail="Variant not found")
    return spec_crud.upsert_specification(db, variant_id, payload)


@router.put("/variants/{variant_id}/ai-attributes", response_model=AIAttributesOut)
def upsert_ai_attributes(variant_id: int, payload: AIAttributesUpdate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    if not crud.get_variant(db, variant_id):
        raise HTTPException(status_code=404, detail="Variant not found")
    return spec_crud.upsert_ai_attributes(db, variant_id, payload)


@router.get("/variants/{variant_id}/ownership-cost", response_model=OwnershipCostBreakdown)
def get_ownership_cost(
    variant_id: int,
    annual_km: float = Query(default=12000, gt=0),
    ownership_years: int = Query(default=5, ge=1, le=15),
    fuel_price_per_unit: float | None = Query(default=None),
    db: Session = Depends(get_db),
):
    """SRS 4.5: purchase price, insurance, fuel, maintenance, road tax, resale, total cost."""
    variant = crud.get_variant(db, variant_id)
    if not variant:
        raise HTTPException(status_code=404, detail="Variant not found")

    params = OwnershipCostInput(annual_km=annual_km, ownership_years=ownership_years, fuel_price_per_unit=fuel_price_per_unit)
    return estimate_ownership_cost(variant, params)
