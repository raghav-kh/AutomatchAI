"""
Scraper for Tata Motors (cars.tatamotors.com), the official manufacturer
site. This is a real, working scraper against real pages -- not a
hypothetical template -- but it comes with two honest limitations you
should know about before assigning it in production:

1. PRICES ARE NOT IN THE STATIC PAGE. cars.tatamotors.com resolves exact
   ex-showroom prices client-side, gated by a city the visitor selects.
   The initial HTML/text never contains a number -- only "Offer Price" /
   "Price *" / "Monthly" placeholders. Every ScrapedVariant this produces
   has price=None. To get real numbers you need either:
     (a) a headless browser (Selenium/Playwright) that selects a city and
         waits for the async price call to resolve -- the SRS's tech
         stack already anticipates this ("Selenium (only if necessary)"),
         or
     (b) a human fills price in via the Catalog UI/API after the fact.
   fuel/transmission ARE inferred here, from the variant name itself (see
   _infer_fuel_and_transmission) -- that's a real signal in the actual
   trim names ("Smart CNG", "Pure + AMT 1.2"), not a guess about the page.

2. THE SITE HAS BOT DETECTION. Requests without a realistic User-Agent,
   or bursts of requests, can get blocked outright. `fetch_html` sets a
   normal browser User-Agent and this scraper should be run with delays
   between models if you add more MODEL_PAGES -- it does not retry on
   its own; a 403/blocked response surfaces as an exception, which the
   dispatcher logs as a failed ScrapeLog rather than silently losing data.

Confirmed structure: tests/fixtures/real_pages/tata_nexon_price_page.txt
is a real capture of cars.tatamotors.com/nexon/ice/price.html.
"""

import re

import requests
from bs4 import BeautifulSoup

from app.pipeline.scrapers.base import BaseScraper
from app.pipeline.scrapers.parsing_utils import parse_variant_blocks
from app.pipeline.schemas import ScrapedCar, ScrapedVariant

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)

# Only models confirmed reachable/parseable as of this writing. Add more
# by fetching the page, confirming the same block shape, and appending here.
MODEL_PAGES = {
    "Nexon": "https://cars.tatamotors.com/nexon/ice/price.html",
}


def _infer_fuel_and_transmission(variant_name: str) -> tuple[str | None, str | None, str | None]:
    """
    Best-effort inference from the trim name text itself -- real signal
    present in names like "Smart CNG" or "Pure + AMT 1.2", not a guess
    about page content. Verify against the spec sheet before trusting
    engine displacement for anything safety-critical.
    """
    name = variant_name.lower()

    if "cng" in name:
        fuel, engine = "CNG", "1199cc"
    elif "1.5" in name:
        fuel, engine = "Diesel", "1497cc"
    elif "1.2" in name:
        fuel, engine = "Petrol", "1199cc"
    else:
        fuel, engine = None, None

    if re.search(r"\bamt\b", name) or re.search(r"\bdca\b", name):
        transmission = "Automatic"
    else:
        transmission = "Manual"

    return fuel, transmission, engine


class TataScraper(BaseScraper):
    manufacturer_name = "Tata Motors"
    base_url = "https://cars.tatamotors.com"

    def fetch_html(self, url: str) -> str:
        resp = requests.get(url, timeout=10, headers={"User-Agent": USER_AGENT})
        resp.raise_for_status()
        return resp.text

    @staticmethod
    def html_to_visible_text(html: str) -> str:
        """
        parse_variant_blocks operates on rendered/visible text (the shape
        you'd get reading the page), not raw markup -- strip tags/scripts
        the same way a text extractor would, so scrape() and the tests
        (which feed captured visible text directly) exercise the same
        parsing path.
        """
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script", "style"]):
            tag.decompose()
        return soup.get_text(separator="\n")

    def parse_page_text(self, model: str, url: str, text: str) -> ScrapedCar:
        blocks = parse_variant_blocks(text)
        variants = []
        for name, features in blocks:
            fuel, transmission, engine = _infer_fuel_and_transmission(name)
            variants.append(
                ScrapedVariant(
                    variant_name=name,
                    price=None,  # see module docstring -- not present in static content
                    fuel=fuel,
                    transmission=transmission,
                    engine=engine,
                    source_url=url,
                )
            )
        return ScrapedCar(model=model, body_type="SUV", variants=variants)

    def scrape(self) -> list[ScrapedCar]:
        cars = []
        for model, url in MODEL_PAGES.items():
            html = self.fetch_html(url)
            text = self.html_to_visible_text(html)
            cars.append(self.parse_page_text(model, url, text))
        return cars
