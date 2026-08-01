from pathlib import Path

from app.pipeline.scrapers.parsing_utils import parse_variant_blocks

FIXTURE = Path(__file__).parent / "fixtures" / "real_pages" / "tata_nexon_price_page.txt"

EXPECTED_NAMES = [
    "Pure + 1.2",
    "Smart 1.2",
    "Smart + AMT 1.2",
    "Pure + AMT 1.2",
    "Smart CNG",
    "Creative + PS DT 1.2",
    "Fearless + PS DT 1.2",
]


def test_extracts_all_real_variant_names_in_order():
    text = FIXTURE.read_text()
    blocks = parse_variant_blocks(text)
    names = [name for name, _ in blocks]
    assert names == EXPECTED_NAMES


def test_extracts_non_empty_feature_lists():
    text = FIXTURE.read_text()
    blocks = dict(parse_variant_blocks(text))
    assert len(blocks["Pure + 1.2"]) == 14
    assert "6 Speed Manual Transmission" in blocks["Pure + 1.2"]
    assert len(blocks["Fearless + PS DT 1.2"]) == 29
    assert "Panoramic Sunroof" not in blocks["Pure + 1.2"]  # features aren't bleeding across blocks


def test_ignores_page_chrome_and_noise_lines():
    text = FIXTURE.read_text()
    names = [name for name, _ in parse_variant_blocks(text)]
    noise = {"Offer Price", "Price", "Price *", "Monthly", "Spinner", "Fuel Type", "Edition"}
    assert not (set(names) & noise)


def test_empty_text_returns_no_blocks():
    assert parse_variant_blocks("") == []


def test_text_with_no_offer_price_marker_returns_no_blocks():
    assert parse_variant_blocks("Some Variant Name\nSome random feature\n") == []
