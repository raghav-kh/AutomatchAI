from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud import manufacturer as crud
from app.crud import scrape_log as scrape_log_crud
from app.models.manufacturer import DataSourceType
from app.models.user import User
from app.api.deps import require_admin
from app.schemas.manufacturer import ManufacturerCreate, ManufacturerUpdate, ManufacturerOut
from app.schemas.scrape_log import ScrapeLogCreate, ScrapeLogOut

router = APIRouter(prefix="/manufacturers", tags=["Manufacturers"])


@router.get("/pending-classification", response_model=list[ManufacturerOut])
def pending_classification(db: Session = Depends(get_db)):
    """
    Manufacturers nobody has checked yet: has an open API? if not, who
    owns the scraper? This is the queue the ingestion pipeline (Phase 2)
    should work through.
    """
    return [m for m in crud.list_manufacturers(db, limit=1000) if m.data_source_type == DataSourceType.UNKNOWN]


@router.post("", response_model=ManufacturerOut, status_code=201)
def create_manufacturer(payload: ManufacturerCreate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    if crud.get_manufacturer_by_name(db, payload.name):
        raise HTTPException(status_code=409, detail="Manufacturer with this name already exists")
    return crud.create_manufacturer(db, payload)


@router.get("", response_model=list[ManufacturerOut])
def list_manufacturers(
    skip: int = 0,
    limit: int = Query(default=100, le=500),
    only_active: bool = False,
    db: Session = Depends(get_db),
):
    return crud.list_manufacturers(db, skip=skip, limit=limit, only_active=only_active)


@router.get("/{manufacturer_id}", response_model=ManufacturerOut)
def get_manufacturer(manufacturer_id: int, db: Session = Depends(get_db)):
    obj = crud.get_manufacturer(db, manufacturer_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Manufacturer not found")
    return obj


@router.patch("/{manufacturer_id}", response_model=ManufacturerOut)
def update_manufacturer(manufacturer_id: int, payload: ManufacturerUpdate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    obj = crud.get_manufacturer(db, manufacturer_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Manufacturer not found")
    return crud.update_manufacturer(db, obj, payload)


@router.delete("/{manufacturer_id}", status_code=204)
def delete_manufacturer(manufacturer_id: int, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    obj = crud.get_manufacturer(db, manufacturer_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Manufacturer not found")
    crud.delete_manufacturer(db, obj)


@router.get("/{manufacturer_id}/scrape-logs", response_model=list[ScrapeLogOut])
def list_scrape_logs(manufacturer_id: int, db: Session = Depends(get_db)):
    if not crud.get_manufacturer(db, manufacturer_id):
        raise HTTPException(status_code=404, detail="Manufacturer not found")
    return scrape_log_crud.list_logs_for_manufacturer(db, manufacturer_id)


@router.post("/{manufacturer_id}/scrape-logs", response_model=ScrapeLogOut, status_code=201)
def create_scrape_log(manufacturer_id: int, payload: ScrapeLogCreate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    """
    Record a pipeline run for this manufacturer. In Phase 2 this will be
    called automatically by the ingestion pipeline (API client or scraper);
    for now it lets us track runs manually/manually-triggered.
    """
    if not crud.get_manufacturer(db, manufacturer_id):
        raise HTTPException(status_code=404, detail="Manufacturer not found")
    return scrape_log_crud.create_log(db, manufacturer_id, payload)
