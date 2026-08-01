import httpx

from app.pipeline.api_probe import probe_manufacturer_api


def test_probe_detects_json_api():
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/api/vehicles":
            return httpx.Response(200, json={"vehicles": []}, headers={"content-type": "application/json"})
        return httpx.Response(404)

    client = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://example-oem.com")
    # probe builds full URLs itself from `website`, so pass base url directly
    result = probe_manufacturer_api("https://example-oem.com", client=client)
    assert result.has_api is True
    assert result.endpoint == "https://example-oem.com/api/vehicles"
    assert result.confidence > 0


def test_probe_no_api_found():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(404)

    client = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://no-api-oem.com")
    result = probe_manufacturer_api("https://no-api-oem.com", client=client)
    assert result.has_api is False


def test_probe_no_website():
    result = probe_manufacturer_api(None)
    assert result.has_api is False
    assert result.confidence == 0.0


def test_probe_ignores_non_json_200():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, text="<html>not json</html>", headers={"content-type": "text/html"})

    client = httpx.Client(transport=httpx.MockTransport(handler), base_url="https://html-only-oem.com")
    result = probe_manufacturer_api("https://html-only-oem.com", client=client)
    assert result.has_api is False
