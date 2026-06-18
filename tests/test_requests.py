"""Integration tests for the requests endpoints."""


def _auth(token):
    return {"Authorization": f"Bearer {token}"}


def test_create_and_list_request(client, tenant_token):
    resp = client.post(
        "/api/requests",
        headers=_auth(tenant_token),
        json={
            "tenant_name": "Olena",
            "address": "Shevchenka 1",
            "work_type": "electrical",
            "description": "No light in the kitchen",
            "volume_hours": 3,
        },
    )
    assert resp.status_code == 201
    created = resp.json()
    assert created["status"] == "new"

    resp = client.get("/api/requests", headers=_auth(tenant_token))
    assert resp.status_code == 200
    assert len(resp.json()) == 1


def test_tenant_cannot_delete_request(client, tenant_token):
    created = client.post(
        "/api/requests",
        headers=_auth(tenant_token),
        json={
            "tenant_name": "Olena",
            "address": "Shevchenka 1",
            "work_type": "plumbing",
            "volume_hours": 2,
        },
    ).json()
    resp = client.delete(f"/api/requests/{created['id']}", headers=_auth(tenant_token))
    assert resp.status_code == 403


def test_dispatcher_can_delete_request(client, tenant_token, dispatcher_token):
    created = client.post(
        "/api/requests",
        headers=_auth(tenant_token),
        json={
            "tenant_name": "Olena",
            "address": "Shevchenka 1",
            "work_type": "plumbing",
            "volume_hours": 2,
        },
    ).json()
    resp = client.delete(
        f"/api/requests/{created['id']}", headers=_auth(dispatcher_token)
    )
    assert resp.status_code == 204


def test_request_validation_error(client, tenant_token):
    resp = client.post(
        "/api/requests",
        headers=_auth(tenant_token),
        json={"tenant_name": "O", "address": "A", "work_type": "x", "volume_hours": 0},
    )
    assert resp.status_code == 422
