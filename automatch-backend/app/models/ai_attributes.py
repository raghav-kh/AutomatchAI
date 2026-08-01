from sqlalchemy import Float, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class AIAttributes(Base):
    """
    Derived/curated scores (0-10 scale unless noted) that the Phase 2
    scoring + LLM explanation engine will consume. These are populated
    either manually, heuristically from specifications, or by an LLM
    pass over manufacturer copy -- not decided yet, out of scope for
    this phase.
    """

    __tablename__ = "ai_attributes"

    id: Mapped[int] = mapped_column(primary_key=True)
    variant_id: Mapped[int] = mapped_column(ForeignKey("variants.id"), unique=True, nullable=False)

    ride_quality: Mapped[float | None] = mapped_column(Float)
    city_friendliness: Mapped[float | None] = mapped_column(Float)
    highway_comfort: Mapped[float | None] = mapped_column(Float)
    maintenance_level: Mapped[float | None] = mapped_column(Float)  # lower = cheaper to maintain
    resale_value: Mapped[float | None] = mapped_column(Float)
    service_network: Mapped[float | None] = mapped_column(Float)
    beginner_friendly: Mapped[bool | None] = mapped_column(Boolean)
    family_score: Mapped[float | None] = mapped_column(Float)
    elderly_friendly: Mapped[bool | None] = mapped_column(Boolean)
    premium_feel: Mapped[float | None] = mapped_column(Float)
    offroad_capability: Mapped[float | None] = mapped_column(Float)

    variant: Mapped["Variant"] = relationship(back_populates="ai_attributes")
