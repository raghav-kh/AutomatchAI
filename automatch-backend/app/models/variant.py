from datetime import datetime

from sqlalchemy import String, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Variant(Base):
    __tablename__ = "variants"

    id: Mapped[int] = mapped_column(primary_key=True)
    car_id: Mapped[int] = mapped_column(ForeignKey("cars.id"), nullable=False)

    variant_name: Mapped[str] = mapped_column(String(120), nullable=False)
    price: Mapped[float | None] = mapped_column(Float)  # ex-showroom, in INR
    transmission: Mapped[str | None] = mapped_column(String(30))  # Manual, Automatic, AMT, CVT, DCT
    fuel: Mapped[str | None] = mapped_column(String(30))  # Petrol, Diesel, CNG, Electric, Hybrid
    engine: Mapped[str | None] = mapped_column(String(50))  # e.g. "1197cc"
    power: Mapped[str | None] = mapped_column(String(30))  # e.g. "88 bhp"
    torque: Mapped[str | None] = mapped_column(String(30))  # e.g. "115 Nm"
    mileage: Mapped[float | None] = mapped_column(Float)  # kmpl or km/full-charge

    # --- Provenance / staleness tracking ---
    raw_source_url: Mapped[str | None] = mapped_column(
        String(500),
        comment="Exact page/API URL this variant's data was pulled from. Lets us trace any "
        "price/spec back to its source and detect when a manufacturer has updated it.",
    )
    last_verified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        comment="Last time this variant's data was confirmed fresh against raw_source_url.",
    )

    car: Mapped["Car"] = relationship(back_populates="variants")
    specifications: Mapped["Specification"] = relationship(
        back_populates="variant", uselist=False, cascade="all, delete-orphan"
    )
    ai_attributes: Mapped["AIAttributes"] = relationship(
        back_populates="variant", uselist=False, cascade="all, delete-orphan"
    )
