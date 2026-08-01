def test_create_manufacturer(client):
    resp = client.post("/manufacturers", json={"name": "Tata Motors", "country": "India"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Tata Motors"
    assert data["data_source_type"] == "unknown"


def test_duplicate_manufacturer_rejected(client):
    client.post("/manufacturers", json={"name": "Citroen", "country": "France"})
    resp = client.post("/manufacturers", json={"name": "Citroen", "country": "France"})
    assert resp.status_code == 409


def test_pending_classification_lists_unknown_source(client):
    client.post("/manufacturers", json={"name": "MG Motor", "country": "UK"})
    client.post(
        "/manufacturers",
        json={"name": "Skoda", "country": "Czech Republic", "data_source_type": "scraper"},
    )
    resp = client.get("/manufacturers/pending-classification")
    names = [m["name"] for m in resp.json()]
    assert "MG Motor" in names
    assert "Skoda" not in names


def test_update_manufacturer_pipeline_metadata(client):
    created = client.post("/manufacturers", json={"name": "Hyundai", "country": "South Korea"}).json()
    resp = client.patch(
        f"/manufacturers/{created['id']}",
        json={
            "data_source_type": "api",
            "has_open_api": True,
            "api_endpoint": "https://api.hyundai.example/v1",
            "confidence_score": 0.95,
        },
    )
    assert resp.status_code == 200
    assert resp.json()["has_open_api"] is True
    assert resp.json()["confidence_score"] == 0.95


def test_confidence_score_out_of_range_rejected(client):
    resp = client.post("/manufacturers", json={"name": "Force Motors", "confidence_score": 1.5})
    assert resp.status_code == 422


def test_scrape_log_recorded(client):
    created = client.post("/manufacturers", json={"name": "Renault", "country": "France"}).json()
    log_resp = client.post(
        f"/manufacturers/{created['id']}/scrape-logs",
        json={"source_type": "scraper", "status": "success", "records_found": 12, "records_saved": 12},
    )
    assert log_resp.status_code == 201
    logs = client.get(f"/manufacturers/{created['id']}/scrape-logs").json()
    assert len(logs) == 1
    assert logs[0]["records_saved"] == 12


def test_get_missing_manufacturer_404(client):
    resp = client.get("/manufacturers/999")
    assert resp.status_code == 404
