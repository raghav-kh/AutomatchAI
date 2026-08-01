from sqlalchemy.orm import Session

from app.models.scrape_log import ScrapeLog
from app.schemas.scrape_log import ScrapeLogCreate


def list_logs_for_manufacturer(db: Session, manufacturer_id: int) -> list[ScrapeLog]:
    return (
        db.query(ScrapeLog)
        .filter(ScrapeLog.manufacturer_id == manufacturer_id)
        .order_by(ScrapeLog.started_at.desc())
        .all()
    )


def create_log(db: Session, manufacturer_id: int, data: ScrapeLogCreate) -> ScrapeLog:
    obj = ScrapeLog(manufacturer_id=manufacturer_id, **data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj
