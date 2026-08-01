from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Car(Base):
    __tablename__ = "cars"

    id: Mapped[int] = mapped_column(primary_key=True)
    manufacturer_id: Mapped[int] = mapped_column(ForeignKey("manufacturers.id"), nullable=False)

    model: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    body_type: Mapped[str | None] = mapped_column(String(50))  # SUV, Hatchback, Sedan, MPV, etc.
    launch_year: Mapped[int | None] = mapped_column(Integer)

    manufacturer: Mapped["Manufacturer"] = relationship(back_populates="cars")
    variants: Mapped[list["Variant"]] = relationship(back_populates="car", cascade="all, delete-orphan")
