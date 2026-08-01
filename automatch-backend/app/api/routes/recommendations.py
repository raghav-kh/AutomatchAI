from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.preferences import UserPreferences
from app.schemas.recommendation import RecommendationOut
from app.recommendation.engine import recommend

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.post("", response_model=list[RecommendationOut])
def get_recommendations(
    prefs: UserPreferences,
    top_n: int = Query(default=10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    """
    Runs the full recommendation pipeline (SRS Section 9): filters
    candidates by budget/fuel/transmission/body type, scores every
    candidate against the stated preferences, and returns the top N
    ranked results with reasons, trade-offs, a confidence score, and an
    explanation (LLM-generated if GROQ_API_KEY is set, template-based
    otherwise).
    """
    return recommend(db, prefs, top_n=top_n)
