"""
Sanity check for LLM-generated explanations. The scoring engine is the
source of truth (SRS 13: "deterministic filtering with LLM reasoning" --
the LLM explains, it doesn't score). If Groq praises something that the
scoring engine flagged as a weak point (e.g. calls a small service network
"excellent" when service_network scored <=4.5), that's the LLM drifting
from the actual data, and we should not surface it -- fall back to the
template instead.

This is a coarse keyword/proximity heuristic, not a semantic check. It
will not catch every contradiction, but it catches the clearest ones
cheaply and without another model call.
"""

import re

COMPONENT_KEYWORDS: dict[str, list[str]] = {
    "budget_fit": ["budget", "price", "afford", "value for money"],
    "safety": ["safety", "airbag", "crash", "ncap"],
    "family_fit": ["family", "seating", "seats"],
    "city_comfort": ["city driving", "city traffic", "maneuverab"],
    "highway_comfort": ["highway", "cruising", "long drive", "long trip"],
    "maintenance": ["maintenance", "running cost", "upkeep", "servicing cost"],
    "resale_value": ["resale"],
    "service_network": ["service network", "service centre", "service center"],
    "fuel_match": ["fuel efficiency", "mileage", "fuel economy"],
    "transmission_match": ["transmission", "gearbox"],
    "parking_fit": ["park", "compact size", "tight spaces"],
}

POSITIVE_MARKERS = [
    "excellent",
    "great",
    "strong",
    "impressive",
    "outstanding",
    "superb",
    "best-in-class",
    "top-notch",
    "exceptional",
    "wide",
    "extensive",
    "class-leading",
]

_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")


def is_consistent(explanation: str, weak_component_keys: list[str]) -> bool:
    """
    Returns False if `explanation` appears to praise (in the same sentence)
    a component that the scoring engine flagged as a trade-off for this
    variant. `weak_component_keys` should come from
    reasons.trade_off_component_keys(trade_offs).
    """
    if not weak_component_keys or not explanation:
        return True

    lowered = explanation.lower()
    sentences = _SENTENCE_SPLIT_RE.split(lowered)

    for key in weak_component_keys:
        keywords = COMPONENT_KEYWORDS.get(key, [])
        for sentence in sentences:
            if any(kw in sentence for kw in keywords) and any(pm in sentence for pm in POSITIVE_MARKERS):
                return False

    return True
