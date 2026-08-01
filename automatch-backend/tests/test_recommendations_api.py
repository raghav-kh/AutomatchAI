import pytest


@pytest.fixture()
def seeded_catalog(client):
    """Two manufacturers, a few cars/variants spanning budget/fuel/body-type so ranking is meaningful."""
    tata = client.post("/manufacturers", json={"name": "Tata Motors", "confidence_score": 0.6}).json()
    mahindra = client.post("/manufacturers", json={"name": "Mahindra", "confidence_score": 0.9}).json()

    nexon = client.post(
        "/cars", json={"model": "Nexon", "body_type": "SUV", "manufacturer_id": tata["id"]}
    ).json()
    client.post(
        f"/cars/{nexon['id']}/variants",
        json={
            "variant_name": "XZ Plus",
            "price": 950000,
            "fuel": "Petrol",
            "transmission": "Manual",
            "mileage": 17.5,
            "specifications": {"seating": 5, "safety_rating": 5, "length": 3993},
            "ai_attributes": {
                "family_score": 7.0,
                "city_friendliness": 8.0,
                "highway_comfort": 6.0,
                "maintenance_level": 3.0,
                "resale_value": 7.0,
                "service_network": 8.0,
            },
        },
    )

    xuv = client.post(
        "/cars", json={"model": "XUV700", "body_type": "SUV", "manufacturer_id": mahindra["id"]}
    ).json()
    client.post(
        f"/cars/{xuv['id']}/variants",
        json={
            "variant_name": "AX7L",
            "price": 2400000,  # far over a modest budget
            "fuel": "Diesel",
            "transmission": "Automatic",
            "mileage": 14.0,
            "specifications": {"seating": 7, "safety_rating": 5, "length": 4695},
            "ai_attributes": {
                "family_score": 9.0,
                "city_friendliness": 5.0,
                "highway_comfort": 9.0,
                "maintenance_level": 5.0,
                "resale_value": 8.0,
                "service_network": 9.0,
            },
        },
    )

    ev = client.post(
        "/cars", json={"model": "Nexon EV", "body_type": "SUV", "manufacturer_id": tata["id"]}
    ).json()
    client.post(
        f"/cars/{ev['id']}/variants",
        json={
            "variant_name": "Long Range",
            "price": 1600000,
            "fuel": "Electric",
            "transmission": "Automatic",
            "specifications": {"seating": 5, "safety_rating": 5, "length": 3993},
            "ai_attributes": {"family_score": 6.0, "city_friendliness": 9.0, "highway_comfort": 5.0},
        },
    )

    return {"tata": tata, "mahindra": mahindra}


def test_recommendations_returns_ranked_results_within_budget(client, seeded_catalog):
    resp = client.post("/recommendations", json={"budget": 1000000, "family_members": 4})
    assert resp.status_code == 200
    results = resp.json()
    assert len(results) >= 1
    # Nexon petrol should outrank the far-over-budget XUV700
    top_model = results[0]["car"]["model"]
    assert top_model == "Nexon"


def test_recommendations_include_explanation_and_confidence(client, seeded_catalog):
    resp = client.post("/recommendations", json={"budget": 1000000})
    results = resp.json()
    top = results[0]
    assert 0 <= top["confidence"] <= 100
    assert top["explanation_source"] == "template"  # no GROQ_API_KEY in test env
    assert isinstance(top["explanation"], str) and len(top["explanation"]) > 0
    assert isinstance(top["reasons"], list) and len(top["reasons"]) > 0


def test_recommendations_short_commute_penalizes_ev(client, seeded_catalog):
    resp = client.post(
        "/recommendations", json={"budget": 2000000, "daily_running_km": 8}
    )
    results = resp.json()
    ev_result = next((r for r in results if r["variant"]["fuel"] == "Electric"), None)
    petrol_result = next((r for r in results if r["car"]["model"] == "Nexon"), None)
    assert ev_result is not None and petrol_result is not None
    assert ev_result["score_breakdown"]["fuel_match"] < petrol_result["score_breakdown"]["fuel_match"]


def test_recommendations_respects_fuel_preference_filter(client, seeded_catalog):
    resp = client.post("/recommendations", json={"budget": 3000000, "fuel_preference": "Diesel"})
    results = resp.json()
    assert all(r["variant"]["fuel"] == "Diesel" for r in results)


def test_recommendations_family_of_seven_favors_seven_seater(client, seeded_catalog):
    resp = client.post("/recommendations", json={"budget": 3000000, "family_members": 7})
    results = resp.json()
    top = results[0]
    assert top["car"]["model"] == "XUV700"


def test_recommendations_empty_when_nothing_matches(client, seeded_catalog):
    resp = client.post("/recommendations", json={"budget": 100})  # nothing this cheap exists
    assert resp.status_code == 200
    assert resp.json() == []
