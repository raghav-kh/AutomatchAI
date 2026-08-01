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

# Manufacturers sold in the Indian market as of the SRS's target scope.
# Extend this list freely -- it's just names/country, everything else is
# discovered by the pipeline.
MANUFACTURERS = [
    ("Maruti Suzuki", "India"),
    ("Hyundai", "South Korea"),
    ("Tata Motors", "India"),
    ("Mahindra", "India"),
    ("Kia", "South Korea"),
    ("Toyota", "Japan"),
    ("Honda", "Japan"),
    ("Renault", "France"),
    ("Nissan", "Japan"),
    ("Skoda", "Czech Republic"),
    ("Volkswagen", "Germany"),
    ("MG Motor", "UK/China"),
    ("Citroen", "France"),
    ("Jeep", "USA"),
    ("BYD", "China"),
    ("Mercedes-Benz", "Germany"),
    ("BMW", "Germany"),
    ("Audi", "Germany"),
    ("Volvo", "Sweden"),
    ("Lexus", "Japan"),
    ("Jaguar", "UK"),
    ("Land Rover", "UK"),
    ("Force Motors", "India"),
    ("Isuzu", "Japan"),
]


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    added, skipped = 0, 0
    try:
        for name, country in MANUFACTURERS:
            exists = db.query(Manufacturer).filter(Manufacturer.name == name).first()
            if exists:
                skipped += 1
                continue
            db.add(Manufacturer(name=name, country=country))
            added += 1
        db.commit()
    finally:
        db.close()
    print(f"Seed complete: {added} added, {skipped} already present.")


if __name__ == "__main__":
    seed()
