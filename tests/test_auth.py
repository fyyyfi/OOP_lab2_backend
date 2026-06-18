"""Integration tests for authentication and authorisation."""


def test_register_and_login(client):
    resp = client.post(
        "/api/auth/register",
        json={
            "username": "newuser",
            "full_name": "New User",
            "password": "pass1234",
            "role": "tenant",
        },
    )
    assert resp.status_code == 201

    resp = client.post(
        "/api/auth/login", json={"username": "newuser", "password": "pass1234"}
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["token_type"] == "bearer"
    assert body["role"] == "tenant"
    assert body["access_token"]


def test_login_with_wrong_password(client):
    client.post(
        "/api/auth/register",
        json={
            "username": "u2",
            "full_name": "U2",
            "password": "rightpass",
            "role": "tenant",
        },
    )
    resp = client.post(
        "/api/auth/login", json={"username": "u2", "password": "wrongpass"}
    )
    assert resp.status_code == 401


def test_protected_endpoint_requires_token(client):
    assert client.get("/api/requests").status_code == 401


def test_me_endpoint(client, tenant_token):
    resp = client.get(
        "/api/auth/me", headers={"Authorization": f"Bearer {tenant_token}"}
    )
    assert resp.status_code == 200
    assert resp.json()["role"] == "tenant"
