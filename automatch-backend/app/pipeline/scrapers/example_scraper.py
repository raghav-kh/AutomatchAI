"""
Template scraper -- copy this file per manufacturer (e.g. tata.py,
mahindra.py) and adjust the URL + CSS selectors for that site's actual
markup. This one is deliberately generic and configurable so it can also
be unit-tested against a static HTML fixture instead of a live site.

Real manufacturer sites vary wildly in structure -- this class assumes a
simple "listing page with repeated car blocks" shape as a starting point,
not a universal solution.
"""

import requests
from bs4 import BeautifulSoup

from app.pipeline.scrapers.base import BaseScraper
from app.pipeline.schemas import ScrapedCar, ScrapedVariant


class GenericListingScraper(BaseScraper):
    """
    Scrapes a single listing page where each car is a block containing a
    model name, optional body type / price, matched via CSS selectors.

    Usage (per manufacturer, in that manufacturer's own scraper file):

        class TataScraper(GenericListingScraper):
            manufacturer_name = "Tata Motors"
            base_url = "https://www.tatamotors.com/cars/"
            car_block_selector = ".car-card"
            model_selector = ".car-card__title"
            price_selector = ".car-card__price"
    """

    manufacturer_name = "Generic"
    base_url = ""

    car_block_selector = ".car-card"
    model_selector = ".car-card__title"
    price_selector = ".car-card__price"
    body_type_selector = ".car-card__body-type"

    def fetch_html(self) -> str:
        resp = requests.get(self.base_url, timeout=10, headers={"User-Agent": "AutoMatchAI-Bot/0.1"})
        resp.raise_for_status()
        return resp.text

    def parse(self, html: str) -> list[ScrapedCar]:
        soup = BeautifulSoup(html, "html.parser")
        cars: list[ScrapedCar] = []

        for block in soup.select(self.car_block_selector):
            model_el = block.select_one(self.model_selector)
            if not model_el:
                continue
            model_name = model_el.get_text(strip=True)

            price = None
            price_el = block.select_one(self.price_selector)
            if price_el:
                price = self._parse_price(price_el.get_text(strip=True))

            body_type = None
            body_type_el = block.select_one(self.body_type_selector)
            if body_type_el:
                body_type = body_type_el.get_text(strip=True)

            cars.append(
                ScrapedCar(
                    model=model_name,
                    body_type=body_type,
                    variants=[
                        ScrapedVariant(
                            variant_name=f"{model_name} (base)",
                            price=price,
                            source_url=self.base_url,
                        )
                    ],
                )
            )

        return cars

    @staticmethod
    def _parse_price(raw: str) -> float | None:
        """e.g. '₹ 8.5 Lakh*' -> 850000.0. Adjust per site's actual format."""
        digits = "".join(c for c in raw if c.isdigit() or c == ".")
        if not digits:
            return None
        try:
            value = float(digits)
        except ValueError:
            return None
        if "lakh" in raw.lower():
            value *= 100_000
        elif "crore" in raw.lower():
            value *= 10_000_000
        return value

    def scrape(self) -> list[ScrapedCar]:
        html = self.fetch_html()
        return self.parse(html)
