"""
Pipeline Steps 6-7 (SRS Section 9): "Send candidates to LLM" and
"Generate explanations". If GROQ_API_KEY isn't set, or the call fails for
any reason, we fall back to a deterministic template built from the same
reasons/trade-offs -- a recommendation should never be blocked on the LLM
being available, per SRS 13: "combines deterministic filtering with LLM
reasoning" rather than depending on it.
"""

import httpx

from app.core.config import settings
from app.models.variant import Variant
from app.models.car import Car
from app.schemas.preferences import UserPreferences
from app.recommendation.groq_client import chat_completion, GroqError
from app.recommendation.explanation_guard import is_consistent
from app.recommendation.reasons import trade_off_component_keys

SYSTEM_PROMPT = (
    "You are AutoMatch AI's explanation engine. Given a car recommendation, "
    "its match reasons, trade-offs, and the buyer's stated preferences, write "
    "a warm, concrete 2-3 sentence explanation of why this car suits them. "
    "Do not invent facts not given to you. Do not use markdown."
)


def _template_explanation(car: Car, variant: Variant, reasons: list[str], trade_offs: list[str]) -> str:
    parts = [f"The {car.model} {variant.variant_name} is recommended because " + ", ".join(r.lower() for r in reasons) + "."]
    if trade_offs:
        parts.append("Worth noting: " + ", ".join(t.lower() for t in trade_offs) + ".")
    return " ".join(parts)


def generate_explanation(
    car: Car,
    variant: Variant,
    prefs: UserPreferences,
    reasons: list[str],
    trade_offs: list[str],
    http_client: httpx.Client | None = None,
) -> tuple[str, str]:
    """Returns (explanation_text, source) where source is 'llm' or 'template'."""
    if not settings.groq_api_key:
        return _template_explanation(car, variant, reasons, trade_offs), "template"

    user_prompt = (
        f"Car: {car.model} {variant.variant_name}, price ~₹{variant.price}, fuel {variant.fuel}, "
        f"transmission {variant.transmission}.\n"
        f"Buyer budget: ₹{prefs.budget}, family members: {prefs.family_members}, "
        f"daily driving: {prefs.daily_running_km} km, highway usage: {prefs.highway_usage.value}.\n"
        f"Match reasons: {', '.join(reasons) if reasons else 'none'}.\n"
        f"Trade-offs: {', '.join(trade_offs) if trade_offs else 'none'}."
    )

    try:
        text = chat_completion(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            client=http_client,
        )
        weak_keys = trade_off_component_keys(trade_offs)
        if not is_consistent(text, weak_keys):
            return _template_explanation(car, variant, reasons, trade_offs), "template"
        return text, "llm"
    except GroqError:
        return _template_explanation(car, variant, reasons, trade_offs), "template"
