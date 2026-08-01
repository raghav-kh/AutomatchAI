"""
API-based ingestion adapter for NHTSA's vPIC (vehicle Product Information
Catalog) API -- a real, free, no-auth-required government API
(vpic.nhtsa.dot.gov). Verified live: GET on a GetModelsForMakeId URL
returns real JSON (see tests/fixtures/real_pages/vpic_aston_martin_models.json,
a genuine captured response, not a hypothetical schema).

HONEST LIMITATION: vPIC is a compliance/identity database (it exists to
support VIN decoding), not a commercial pricing/spec catalog. It gives you
canonical Make/Model names -- genuinely useful for confirming a model
exists and its official name -- but nothing about trims, variants, price,
or specs. Every ScrapedCar this produces has exactly one placeholder
ScrapedVariant with price=None, mirroring how the Tata scraper is honest
about its own gap (see scrapers/tata.py) rather than inventing numbers.

This is also, deliberately, not tied to any specific manufacturer -- unlike
scrapers/tata.py (which targets one hardcoded site), this class is reusable
for ANY make: Manufacturer.api_endpoint holds the ready-to-call URL (e.g.
"https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMakeId/440?format=json"),
discovered by an admin and stored per-manufacturer. That's what BaseApiClient
is for -- see its docstring.

Note for India-market manufacturers: vPIC only covers vehicles
certified/sold in the US, so most Indian-market-only manufacturers (Tata,
Mahindra, etc.) won't appear here. This adapter is a genuine, verified
demonstration of the API-ingestion pattern, not a claim that vPIC covers
your target manufacturers -- swap in whatever real open API a given
manufacturer actually exposes, following this same shape.
"""

import requests

from app.pipeline.scrapers.base import BaseApiClient
from app.pipeline.schemas import ScrapedCar, ScrapedVariant

USER_AGENT = "AutoMatchAI-Bot/0.1 (+https://github.com/raghav-kh/automatch-ai)"


class NhtsaVpicApiClient(BaseApiClient):
    manufacturer_name = "NHTSA vPIC"  # overridden by whichever manufacturer's api_endpoint is configured

    def fetch_json(self) -> dict:
        resp = requests.get(self.api_endpoint, timeout=10, headers={"User-Agent": USER_AGENT})
        resp.raise_for_status()
        return resp.json()

    @staticmethod
    def parse_response(data: dict, source_url: str) -> list[ScrapedCar]:
        results = data.get("Results", [])
        cars: list[ScrapedCar] = []
        seen_models = set()

        for row in results:
            model_name = row.get("Model_Name")
            if not model_name or model_name in seen_models:
                continue
            seen_models.add(model_name)

            cars.append(
                ScrapedCar(
                    model=model_name,
                    variants=[
                        ScrapedVariant(
                            variant_name="Base",  # vPIC has no trim/variant granularity
                            price=None,  # see module docstring -- not a commercial data source
                            source_url=source_url,
                        )
                    ],
                )
            )
        return cars

    def scrape(self) -> list[ScrapedCar]:
        data = self.fetch_json()
        return self.parse_response(data, self.api_endpoint)
