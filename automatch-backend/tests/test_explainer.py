import httpx
import pytest

from app.models.variant import Variant
from app.models.car import Car
from app.schemas.preferences import UserPreferences
from app.recommendation.explainer import generate_explanation
from app.core.config import settings


@pytest.fixture(autouse=True)
def reset_groq_key():
    original = settings.groq_api_key
    yield
    settings.groq_api_key = original


def make_car_and_variant():
    car = Car(id=1, manufacturer_id=1, model="Nexon", body_type="SUV")
    variant = Variant(id=1, car_id=1, variant_name="XZ Plus", price=1250000, fuel="Petrol", transmission="Manual")
    return car, variant


def test_falls_back_to_template_when_no_api_key():
    settings.groq_api_key = None
    car, variant = make_car_and_variant()
    prefs = UserPreferences(budget=1300000)

    text, source = generate_explanation(car, variant, prefs, ["Fits comfortably within your budget"], [])
    assert source == "template"
    assert "Nexon" in text


def test_uses_llm_when_configured_and_call_succeeds():
    settings.groq_api_key = "fake-key-for-test"
    car, variant = make_car_and_variant()
    prefs = UserPreferences(budget=1300000)

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={"choices": [{"message": {"content": "This Nexon variant is a great fit for your budget."}}]},
        )

    client = httpx.Client(transport=httpx.MockTransport(handler))
    text, source = generate_explanation(
        car, variant, prefs, ["Fits comfortably within your budget"], [], http_client=client
    )
    assert source == "llm"
    assert "great fit" in text


def test_falls_back_to_template_when_llm_call_fails():
    settings.groq_api_key = "fake-key-for-test"
    car, variant = make_car_and_variant()
    prefs = UserPreferences(budget=1300000)

    client = httpx.Client(transport=httpx.MockTransport(lambda r: httpx.Response(500)))
    text, source = generate_explanation(
        car, variant, prefs, ["Fits comfortably within your budget"], [], http_client=client
    )
    assert source == "template"
    assert "Nexon" in text


def test_falls_back_to_template_when_llm_contradicts_a_trade_off():
    settings.groq_api_key = "fake-key-for-test"
    car, variant = make_car_and_variant()
    prefs = UserPreferences(budget=1300000)

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "choices": [
                    {"message": {"content": "This Nexon has an excellent service network nationwide."}}
                ]
            },
        )

    client = httpx.Client(transport=httpx.MockTransport(handler))
    text, source = generate_explanation(
        car,
        variant,
        prefs,
        ["Fits comfortably within your budget"],
        ["Smaller service network in some regions"],
        http_client=client,
    )
    assert source == "template"  # LLM text rejected for contradicting the trade-off
    assert "Nexon" in text
