from pydantic import BaseModel


class ComparisonRow(BaseModel):
    variant_id: int
    car_model: str
    variant_name: str
    manufacturer_name: str

    price: float | None
    power: str | None
    torque: str | None
    mileage: float | None

    safety_rating: float | None
    airbags: int | None

    maintenance_level: float | None
    boot_space: float | None
    ground_clearance: float | None
    family_score: float | None  # closest available proxy for "rear seat comfort" (SRS 4.6)

    ai_recommendation_score: float  # neutral-preference score, see comparison.py


class AlternativeSuggestion(BaseModel):
    """SRS 4.7: 'You may also consider the Honda Elevate because...'"""

    variant_id: int
    car_model: str
    variant_name: str
    manufacturer_name: str
    reasons: list[str]
    price_difference: float  # positive = alternative costs more than the reference variant
