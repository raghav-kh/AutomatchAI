"""
Text-pattern parser for manufacturer price/spec pages whose markup repeats
a simple shape: a variant name, followed shortly by a price/CTA block,
followed by a bulleted feature list, followed by the price/CTA block again.

This exists because tatamotors.com's cars.tatamotors.com pricing pages
(and many others in this space) render exact prices client-side, gated by
a selected city -- the static HTML/text never contains the number. Variant
names and feature lists, however, are present in the initial render. This
parser extracts what's actually there instead of pretending the price is
scrapable when it isn't.

Confirmed against a real captured page (see
tests/fixtures/real_pages/tata_nexon_price_page.txt) -- this is not a
hypothetical shape, it's what cars.tatamotors.com/nexon/ice/price.html
actually returns.
"""

import re

# Labels that appear as their own "line" in the extracted text but aren't
# variant names -- price/CTA chrome, page furniture, empty-state copy.
NOISE_LINES = {
    "offer price",
    "price",
    "price *",
    "monthly",
    "spinner",
    "offers",
    "0 offers available",
    "fuel type",
    "transmission type",
    "edition",
    "can't find any results",
    "discover our wide range of financing options",
}

# How many lines ahead of a candidate name we'll scan for the "Offer Price"
# marker that confirms it's actually a variant name, not body copy.
LOOKAHEAD_WINDOW = 4


def parse_variant_blocks(text: str) -> list[tuple[str, list[str]]]:
    """
    Returns [(variant_name, [feature, feature, ...]), ...] in document order.
    A line is treated as a variant name if it's non-empty, isn't in
    NOISE_LINES, isn't a bullet, and is followed within LOOKAHEAD_WINDOW
    lines by an "Offer Price" marker (every real variant block has one).
    """
    lines = [l.rstrip() for l in text.split("\n")]

    candidates: list[tuple[int, str]] = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped or stripped.lower() in NOISE_LINES or stripped.startswith(("•", "-")):
            continue
        lookahead = [l.strip() for l in lines[i + 1 : i + 1 + LOOKAHEAD_WINDOW]]
        if "Offer Price" in lookahead:
            candidates.append((i, stripped))

    blocks: list[tuple[str, list[str]]] = []
    for n, (idx, name) in enumerate(candidates):
        end = candidates[n + 1][0] if n + 1 < len(candidates) else len(lines)
        segment = lines[idx:end]
        features = [
            re.sub(r"^[•\-]\s*", "", l.strip()).strip()
            for l in segment
            if l.strip().startswith(("•", "-"))
        ]
        blocks.append((name, features))

    return blocks
