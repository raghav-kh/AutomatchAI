"""
Heuristic check for "does this manufacturer expose an open/public API we
can hit directly, instead of scraping HTML".

This intentionally takes an injected httpx.Client so it's cheap to unit
test with a mock transport -- no real network calls happen in tests.
"""

import httpx

from app.pipeline.schemas import ProbeResult

# Common paths manufacturers/dealers sometimes expose publicly.
# Extend this list as you discover real ones -- it's a heuristic, not a guarantee.
CANDIDATE_PATHS = [
    "/api/vehicles",
    "/api/models",
    "/api/v1/models",
    "/.well-known/openapi.json",
    "/swagger.json",
]

JSON_CONTENT_TYPES = ("application/json", "application/hal+json", "application/vnd.api+json")


def probe_manufacturer_api(website: str | None, client: httpx.Client | None = None) -> ProbeResult:
    """
    Best-effort check: does `website` (or a subset of common paths on it)
    respond with JSON on a GET request? This is a coarse signal, not proof
    of a stable public API -- a human should confirm before fully trusting
    `has_open_api=True` in production.
    """
    if not website:
        return ProbeResult(has_api=False, confidence=0.0, notes="No website on file to probe")

    owns_client = client is None
    client = client or httpx.Client(timeout=5.0, follow_redirects=True)

    try:
        for path in CANDIDATE_PATHS:
            url = website.rstrip("/") + path
            try:
                resp = client.get(url)
            except httpx.HTTPError as exc:
                continue

            if resp.status_code == 200:
                content_type = resp.headers.get("content-type", "")
                if any(ct in content_type for ct in JSON_CONTENT_TYPES):
                    return ProbeResult(
                        has_api=True,
                        endpoint=url,
                        confidence=0.7,  # heuristic hit; needs human confirmation to reach 1.0
                        notes=f"JSON response at {path}",
                    )

        return ProbeResult(has_api=False, confidence=0.5, notes="No JSON endpoint found among common paths")
    finally:
        if owns_client:
            client.close()
