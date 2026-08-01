"""
SRS 4.4 (Explainable AI) calls for a "Recommendation Confidence" percentage
alongside every result. We treat that as distinct from the match score:
a variant can be a perfect preference match (score) but still deserve a
lower confidence if the underlying data is thin or came from a low-trust
source (Manufacturer.confidence_score, set during pipeline classification).
"""

from app.models.variant import Variant


def _data_completeness(variant: Variant) -> float:
    """Fraction (0-1) of the fields that matter most to scoring that are actually populated."""
    fields_present = 0
    fields_checked = 0

    for value in (variant.price, variant.fuel, variant.transmission, variant.mileage):
        fields_checked += 1
        if value is not None:
            fields_present += 1

    spec = variant.specifications
    for attr in ("safety_rating", "seating", "boot_space", "length"):
        fields_checked += 1
        if spec is not None and getattr(spec, attr, None) is not None:
            fields_present += 1

    ai = variant.ai_attributes
    for attr in ("family_score", "city_friendliness", "highway_comfort", "maintenance_level", "resale_value"):
        fields_checked += 1
        if ai is not None and getattr(ai, attr, None) is not None:
            fields_present += 1

    return fields_present / fields_checked if fields_checked else 0.0


def compute_confidence(variant: Variant, score_total_0_to_10: float) -> float:
    """
    Blends: how well it matches (60%), how complete the underlying data is
    (25%), and how much we trust the manufacturer's data source (15%,
    from Manufacturer.confidence_score -- API-sourced data generally
    trusted more than scraped data). Returns a 0-100 percentage.
    """
    match_component = score_total_0_to_10 / 10
    completeness_component = _data_completeness(variant)

    manufacturer = variant.car.manufacturer if variant.car else None
    trust_component = manufacturer.confidence_score if manufacturer and manufacturer.confidence_score is not None else 0.5

    confidence = (match_component * 0.60 + completeness_component * 0.25 + trust_component * 0.15) * 100
    return round(max(0.0, min(100.0, confidence)), 1)
