"""
Seeds the manufacturers table with names + country only.

data_source_type is left as UNKNOWN for every row on purpose: figuring out
"does this manufacturer expose an open API, or do we need a scraper" is the
Phase 2 pipeline's job (see GET /manufacturers/pending-classification).

Run with:
    python -m scripts.seed_manufacturers
"""

from app.core.database import SessionLocal, Base, engine
from app.models.manufacturer import Manufacturer
from app import models  # noqa: F401
import csv
from pathlib import Path

CSV_FILE = Path(__file__).parent / "manufacturers.csv"

def seed():
    Base.metadata.create_all(bind=engine)

    if not CSV_FILE.exists():
        raise FileNotFoundError(f"CSV not found: {CSV_FILE}")
    db = SessionLocal()

    added = 0
    skipped =0

    try:
        with open (CSV_FILE, newline="",encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                name = row["Manufacturer"].strip()
                country = row["Country"].strip()

                if not name:
                    continue

                exists = (
                    db.query(Manufacturer)
                    .filter(Manufacturer.name == name)
                    .first()
                )

                if exists:
                    exists.country = country
                    skipped += 1
                    continue

                db.add(
                    Manufacturer(
                        name = name,
                        country = country,
                    )
                )

                added += 1
        db.commit()

    finally:
        db.close()

    print(f"Seed complete: {added} added, {skipped} already present .")

if __name__ == "__main__":
    seed()
