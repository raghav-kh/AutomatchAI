from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud import manufacturer as manufacturer_crud
from app.pipeline import dispatcher
from app.schemas.manufacturer import ManufacturerOut
from app.api.deps import require_admin
from pydantic import BaseModel

router = APIRouter(prefix="/pipeline", tags=["Pipeline"], dependencies=[Depends(require_admin)])


class IngestionResultOut(BaseModel):
    cars_found: int
    variants_found: int
    variants_saved: int
    errors: list[str]


@router.post("/classify-pending", response_model=list[ManufacturerOut])
def classify_pending(limit: int | None = None, db: Session = Depends(get_db)):
    """
    Runs the API-detection probe over every manufacturer still marked
    data_source_type=unknown, and updates each with a data_source_type
    and confidence_score. Every run is logged to that manufacturer's
    scrape_logs.
    """
    return dispatcher.classify_pending(db, limit=limit)


@router.post("/manufacturers/{manufacturer_id}/ingest", response_model=IngestionResultOut)
def ingest_manufacturer(manufacturer_id: int, db: Session = Depends(get_db)):
    """
    Runs ingestion for one manufacturer using its assigned scraper_module,
    persisting Car/Variant rows with provenance (raw_source_url,
    last_verified_at). Requires scraper_module to already be set.
    """
    manufacturer = manufacturer_crud.get_manufacturer(db, manufacturer_id)
    if not manufacturer:
        raise HTTPException(status_code=404, detail="Manufacturer not found")

    result = dispatcher.run_ingestion_for_manufacturer(db, manufacturer)
    return IngestionResultOut(
        cars_found=result.cars_found,
        variants_found=result.variants_found,
        variants_saved=result.variants_saved,
        errors=result.errors,
    )
