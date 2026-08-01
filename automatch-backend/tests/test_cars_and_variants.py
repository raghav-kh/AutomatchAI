import pytest


@pytest.fixture()
def manufacturer(client):
    return client.post("/manufacturers", json={"name": "Mahindra", "country": "India"}).json()


def test_create_car_requires_valid_manufacturer(client):
    resp = client.post("/cars", json={"model": "XUV 3XO", "body_type": "SUV", "manufacturer_id": 999})
    assert resp.status_code == 404


def test_create_car_and_fetch_with_variants(client, manufacturer):
    car = client.post(
        "/cars",
        json={"model": "XUV 3XO", "body_type": "SUV", "launch_year": 2024, "manufacturer_id": manufacturer["id"]},
    ).json()
    assert car["manufacturer_id"] == manufacturer["id"]

    variant_payload = {
        "variant_name": "AX7L Turbo",
        "price": 1450000,
        "transmission": "Automatic",
        "fuel": "Petrol",
        "mileage": 18.0,
        "specifications": {"seating": 5, "airbags": 6, "safety_rating": 5, "boot_space": 364},
        "ai_attributes": {"family_score": 8.5, "city_friendliness": 7.0, "elderly_friendly": True},
    }
    v_resp = client.post(f"/cars/{car['id']}/variants", json=variant_payload)
    assert v_resp.status_code == 201
    variant = v_resp.json()
    assert variant["specifications"]["seating"] == 5
    assert variant["ai_attributes"]["family_score"] == 8.5

    car_detail = client.get(f"/cars/{car['id']}").json()
    assert len(car_detail["variants"]) == 1
    assert car_detail["variants"][0]["variant_name"] == "AX7L Turbo"


def test_upsert_specifications_independently(client, manufacturer):
    car = client.post(
        "/cars", json={"model": "Thar Roxx", "body_type": "SUV", "manufacturer_id": manufacturer["id"]}
    ).json()
    variant = client.post(f"/cars/{car['id']}/variants", json={"variant_name": "AX5"}).json()

    resp = client.put(f"/variants/{variant['id']}/specifications", json={"seating": 4, "ground_clearance": 226})
    assert resp.status_code == 200
    assert resp.json()["ground_clearance"] == 226

    # calling again should update, not duplicate
    resp2 = client.put(f"/variants/{variant['id']}/specifications", json={"seating": 5})
    assert resp2.json()["seating"] == 5


def test_filter_cars_by_manufacturer_and_body_type(client, manufacturer):
    client.post("/cars", json={"model": "XUV700", "body_type": "SUV", "manufacturer_id": manufacturer["id"]})
    client.post("/cars", json={"model": "Marazzo", "body_type": "MPV", "manufacturer_id": manufacturer["id"]})

    resp = client.get(f"/cars?manufacturer_id={manufacturer['id']}&body_type=SUV")
    models = [c["model"] for c in resp.json()]
    assert models == ["XUV700"]


def test_delete_car_cascades_variants(client, manufacturer):
    car = client.post("/cars", json={"model": "Bolero", "manufacturer_id": manufacturer["id"]}).json()
    variant = client.post(f"/cars/{car['id']}/variants", json={"variant_name": "B4"}).json()

    client.delete(f"/cars/{car['id']}")
    resp = client.get(f"/variants/{variant['id']}")
    assert resp.status_code == 404


def test_variant_provenance_fields(client, manufacturer):
    car = client.post("/cars", json={"model": "Scorpio-N", "manufacturer_id": manufacturer["id"]}).json()
    variant = client.post(
        f"/cars/{car['id']}/variants",
        json={
            "variant_name": "Z8L",
            "raw_source_url": "https://www.mahindra.com/scorpio-n/z8l",
            "last_verified_at": "2026-07-01T00:00:00Z",
        },
    ).json()
    assert variant["raw_source_url"] == "https://www.mahindra.com/scorpio-n/z8l"
    assert variant["last_verified_at"] is not None


def test_stale_variants_endpoint(client, manufacturer):
    car = client.post("/cars", json={"model": "XUV400", "manufacturer_id": manufacturer["id"]}).json()
    # never verified -> stale
    never_verified = client.post(f"/cars/{car['id']}/variants", json={"variant_name": "EL"}).json()
    # verified long ago -> stale under a 90-day window
    old = client.post(
        f"/cars/{car['id']}/variants",
        json={"variant_name": "EC", "last_verified_at": "2020-01-01T00:00:00Z"},
    ).json()
    # freshly verified -> not stale
    client.post(
        f"/cars/{car['id']}/variants",
        json={"variant_name": "EX", "last_verified_at": "2026-07-28T00:00:00Z"},
    )

    resp = client.get("/variants/stale?days=90")
    stale_ids = {v["id"] for v in resp.json()}
    assert never_verified["id"] in stale_ids
    assert old["id"] in stale_ids
