from app.pipeline.scrapers.base import BaseScraper
from app.pipeline.schemas import ScrapedCar, ScrapedVariant


class FakeTataScraper(BaseScraper):
    manufacturer_name = "Tata Motors"
    base_url = "https://fake-tata.example/lineup"

    def scrape(self) -> list[ScrapedCar]:
        return [
            ScrapedCar(
                model="Nexon",
                body_type="SUV",
                launch_year=2023,
                variants=[
                    ScrapedVariant(
                        variant_name="XZ Plus",
                        price=1250000,
                        fuel="Petrol",
                        transmission="Manual",
                        mileage=17.5,
                        source_url=self.base_url,
                    ),
                    ScrapedVariant(
                        variant_name="XZ Plus (O)",
                        price=1350000,
                        fuel="Diesel",
                        transmission="Automatic",
                        mileage=23.0,
                        source_url=self.base_url,
                    ),
                ],
            )
        ]


class FailingScraper(BaseScraper):
    manufacturer_name = "Broken OEM"
    base_url = "https://broken.example"

    def scrape(self) -> list[ScrapedCar]:
        raise RuntimeError("site markup changed, selectors no longer match")
