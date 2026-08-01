"""
Ties together SRS Section 9's 8-step pipeline:
1. (caller) collect user preferences -> UserPreferences
2-3. filters.get_candidates() -- convert to filters, query DB
4. scoring.score_variant() -- score every candidate
5. select top N
6-7. explainer.generate_explanation() -- LLM (or template fallback)
8. return ranked RecommendationOut list
"""

from sqlalchemy.orm import Session
import httpx

from app.schemas.preferences import UserPreferences
from app.schemas.recommendation import RecommendationOut, ScoreBreakdown
from app.schemas.variant import VariantOut
from app.schemas.car import CarOut
from app.recommendation.filters import get_candidates
from app.recommendation.scoring import score_variant
from app.recommendation.confidence import compute_confidence
from app.recommendation.reasons import build_reasons_and_tradeoffs
from app.recommendation.explainer import generate_explanation


def recommend(
    db: Session,
    prefs: UserPreferences,
    top_n: int = 10,
    http_client: httpx.Client | None = None,
) -> list[RecommendationOut]:
    candidates = get_candidates(db, prefs)

    scored: list[tuple] = []
    for variant in candidates:
        components, total = score_variant(variant, prefs)
        scored.append((variant, components, total))

    # Step 5: select top N candidates
    scored.sort(key=lambda t: t[2], reverse=True)
    top_candidates = scored[:top_n]

    results: list[RecommendationOut] = []
    for variant, components, total in top_candidates:
        confidence = compute_confidence(variant, total)
        reasons, trade_offs = build_reasons_and_tradeoffs(components, prefs)

        car = variant.car
        explanation, source = generate_explanation(
            car, variant, prefs, reasons, trade_offs, http_client=http_client
        )

        results.append(
            RecommendationOut(
                variant=VariantOut.model_validate(variant),
                car=CarOut.model_validate(car),
                manufacturer_name=car.manufacturer.name,
                score_breakdown=ScoreBreakdown(**components.as_dict(), total=total),
                confidence=confidence,
                reasons=reasons,
                trade_offs=trade_offs,
                explanation=explanation,
                explanation_source=source,
            )
        )

    return results
