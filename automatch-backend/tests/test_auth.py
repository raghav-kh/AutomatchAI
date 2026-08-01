from app.core.config import settings


def register_admin(raw_client, username="admin1", password="supersecret123"):
    return raw_client.post(
        "/auth/register",
        json={"username": username, "password": password, "setup_key": settings.admin_setup_key},
    )


def login(raw_client, username="admin1", password="supersecret123"):
    return raw_client.post("/auth/login", data={"username": username, "password": password})


def test_register_rejects_wrong_setup_key(raw_client):
    resp = raw_client.post(
        "/auth/register", json={"username": "admin1", "password": "supersecret123", "setup_key": "wrong-key"}
    )
    assert resp.status_code == 403


def test_register_succeeds_with_correct_setup_key(raw_client):
    resp = register_admin(raw_client)
    assert resp.status_code == 201
    body = resp.json()
    assert body["username"] == "admin1"
    assert body["is_admin"] is True
    assert "hashed_password" not in body
    assert "password" not in body


def test_register_rejects_duplicate_username(raw_client):
    register_admin(raw_client)
    resp = register_admin(raw_client)
    assert resp.status_code == 409


def test_register_rejects_short_password(raw_client):
    resp = raw_client.post(
        "/auth/register", json={"username": "admin2", "password": "short", "setup_key": settings.admin_setup_key}
    )
    assert resp.status_code == 422


def test_login_succeeds_and_returns_bearer_token(raw_client):
    register_admin(raw_client)
    resp = login(raw_client)
    assert resp.status_code == 200
    body = resp.json()
    assert body["token_type"] == "bearer"
    assert len(body["access_token"]) > 20


def test_login_rejects_wrong_password(raw_client):
    register_admin(raw_client)
    resp = login(raw_client, password="wrongpassword")
    assert resp.status_code == 401


def test_login_rejects_unknown_username(raw_client):
    resp = login(raw_client, username="ghost")
    assert resp.status_code == 401


def test_me_requires_token(raw_client):
    resp = raw_client.get("/auth/me")
    assert resp.status_code == 401


def test_me_returns_current_user_with_valid_token(raw_client):
    register_admin(raw_client)
    token = login(raw_client).json()["access_token"]
    resp = raw_client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.json()["username"] == "admin1"


def test_me_rejects_garbage_token(raw_client):
    resp = raw_client.get("/auth/me", headers={"Authorization": "Bearer not-a-real-token"})
    assert resp.status_code == 401


def test_write_endpoint_rejected_without_token(raw_client):
    resp = raw_client.post("/manufacturers", json={"name": "Tata Motors"})
    assert resp.status_code == 401


def test_write_endpoint_succeeds_with_valid_token(raw_client):
    register_admin(raw_client)
    token = login(raw_client).json()["access_token"]
    resp = raw_client.post(
        "/manufacturers", json={"name": "Tata Motors"}, headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 201


def test_read_endpoints_remain_public_without_token(raw_client):
    resp = raw_client.get("/manufacturers")
    assert resp.status_code == 200


def test_pipeline_endpoints_require_auth(raw_client):
    resp = raw_client.post("/pipeline/classify-pending")
    assert resp.status_code == 401


def test_recommendations_endpoint_remains_public(raw_client):
    resp = raw_client.post("/recommendations", json={"budget": 1000000})
    assert resp.status_code == 200
