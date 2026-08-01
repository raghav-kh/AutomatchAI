from sqlalchemy import Integer, Float, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Specification(Base):
    __tablename__ = "specifications"

    id: Mapped[int] = mapped_column(primary_key=True)
    variant_id: Mapped[int] = mapped_column(ForeignKey("variants.id"), unique=True, nullable=False)

    seating: Mapped[int | None] = mapped_column(Integer)
    airbags: Mapped[int | None] = mapped_column(Integer)
    safety_rating: Mapped[float | None] = mapped_column(Float)  # e.g. Global NCAP stars
    ground_clearance: Mapped[float | None] = mapped_column(Float)  # mm
    boot_space: Mapped[float | None] = mapped_column(Float)  # litres
    wheelbase: Mapped[float | None] = mapped_column(Float)  # mm
    length: Mapped[float | None] = mapped_column(Float)  # mm
    width: Mapped[float | None] = mapped_column(Float)  # mm
    height: Mapped[float | None] = mapped_column(Float)  # mm

    variant: Mapped["Variant"] = relationship(back_populates="specifications")
