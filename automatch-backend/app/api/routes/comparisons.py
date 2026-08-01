from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud import variant as variant_crud
from app.schemas.comparison import ComparisonRow, AlternativeSuggestion
from app.recommendation.comparison import compare_variants
from app.recommendation.alternative import find_alternatives

router = APIRouter(tags=["Comparisons"])


@router.get("/compare", response_model=list[ComparisonRow])
def compare(variant_ids: list[int] = Query(..., min_length=2, max_length=10), db: Session = Depends(get_db)):
    """SRS 4.6: side-by-side comparison across performance, safety, maintenance, and AI score."""
    try:
        return compare_variants(db, variant_ids)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.get("/variants/{variant_id}/alternatives", response_model=list[AlternativeSuggestion])
def alternatives(variant_id: int, limit: int = Query(default=3, ge=1, le=10), db: Session = Depends(get_db)):
    """SRS 4.7: 'You may also consider X because...' for a variant the user has selected."""
    reference = variant_crud.get_variant(db, variant_id)
    if not reference:
        raise HTTPException(status_code=404, detail="Variant not found")
    return find_alternatives(db, reference, limit=limit)
