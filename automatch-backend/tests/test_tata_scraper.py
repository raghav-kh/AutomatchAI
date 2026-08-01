from pathlib import Path
from unittest.mock import patch

from app.pipeline.scrapers.tata import TataScraper, _infer_fuel_and_transmission, MODEL_PAGES
from app.pipeline import dispatcher
from app.crud import manufacturer as manufacturer_crud
from app.schemas.manufacturer import ManufacturerCreate

FIXTURE = Path(__file__).parent / "fixtures" / "real_pages" / "tata_nexon_price_page.txt"


def test_infer_fuel_and_transmission_cng():
    fuel, transmission, engine = _infer_fuel_and_transmission("Smart CNG")
    assert fuel == "CNG"
    assert transmission == "Manual"


def test_infer_fuel_and_transmission_amt():
    fuel, transmission, engine = _infer_fuel_and_transmission("Smart + AMT 1.2")
    assert fuel == "Petrol"
    assert transmission == "Automatic"
    assert engine == "1199cc"


def test_infer_fuel_and_transmission_diesel_displacement():
    fuel, transmission, engine = _infer_fuel_and_transmission("Fearless + PS DT 1.5")
    assert fuel == "Diesel"
    assert engine == "1497cc"
    assert transmission == "Manual"


def test_parse_page_text_against_real_fixture():
    scraper = TataScraper()
    text = FIXTURE.read_text()
    car = scraper.parse_page_text("Nexon", "https://cars.tatamotors.com/nexon/ice/price.html", text)

    assert car.model == "Nexon"
    assert len(car.variants) == 7

    smart_amt = next(v for v in car.variants if v.variant_name == "Smart + AMT 1.2")
    assert smart_amt.price is None  # honestly reported as unknown, not guessed
    assert smart_amt.fuel == "Petrol"
    assert smart_amt.transmission == "Automatic"
    assert smart_amt.source_url == "https://cars.tatamotors.com/nexon/ice/price.html"


def test_html_to_visible_text_strips_tags_and_scripts():
    html = """
    <html><body>
      <script>var x = 1;</script>
      <div>Pure + 1.2</div>
      <p>Offer Price</p>
      <ul><li>6 Speed Manual Transmission</li></ul>
    </body></html>
    """
    text = TataScraper.html_to_visible_text(html)
    assert "var x = 1" not in text
    assert "Pure + 1.2" in text
    assert "Offer Price" in text


def test_scrape_end_to_end_with_fetch_mocked():
    scraper = TataScraper()
    fixture_text = FIXTURE.read_text()
    fake_html = f"<html><body><pre>{fixture_text}</pre></body></html>"

    with patch.object(TataScraper, "fetch_html", return_value=fake_html):
        cars = scraper.scrape()

    assert len(cars) == len(MODEL_PAGES)
    nexon = next(c for c in cars if c.model == "Nexon")
    assert len(nexon.variants) == 7


def test_ingestion_pipeline_persists_tata_variants_with_provenance(db_session):
    manufacturer = manufacturer_crud.create_manufacturer(
        db_session,
        ManufacturerCreate(
            name="Tata Motors",
            data_source_type="scraper",
            scraper_module="app.pipeline.scrapers.tata.TataScraper",
        ),
    )

    fixture_text = FIXTURE.read_text()
    fake_html = f"<html><body><pre>{fixture_text}</pre></body></html>"

    with patch.object(TataScraper, "fetch_html", return_value=fake_html):
        result = dispatcher.run_ingestion_for_manufacturer(db_session, manufacturer)

    assert result.cars_found == 1
    assert result.variants_found == 7
    assert result.variants_saved == 7
    assert result.errors == []

    from app.models.car import Car
    from app.models.variant import Variant

    car = db_session.query(Car).filter(Car.manufacturer_id == manufacturer.id).first()
    assert car.model == "Nexon"
    variants = db_session.query(Variant).filter(Variant.car_id == car.id).all()
    assert len(variants) == 7
    assert all(v.raw_source_url == "https://cars.tatamotors.com/nexon/ice/price.html" for v in variants)
    assert all(v.price is None for v in variants)  # honest about the real limitation
    assert all(v.last_verified_at is not None for v in variants)
