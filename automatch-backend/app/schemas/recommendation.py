from pydantic import BaseModel

from app.schemas.variant import VariantOut
from app.schemas.car import CarOut


class ScoreBreakdown(BaseModel):
    budget_fit: float
    safety: float
    family_fit: float
    city_comfort: float
    highway_comfort: float
    maintenance: float
    resale_value: float
    service_network: float
    fuel_match: float
    transmission_match: float
    parking_fit: float
    total: float


class RecommendationOut(BaseModel):
    variant: VariantOut
    car: CarOut
    manufacturer_name: str

    score_breakdown: ScoreBreakdown
    confidence: float  # 0-100, blends data completeness + score + manufacturer data trust
    reasons: list[str]  # "Recommended because: ..." bullets
    trade_offs: list[str]
    explanation: str  # short natural-language summary (LLM-generated if Groq configured, else templated)
    explanation_source: str  # "llm" | "template"
