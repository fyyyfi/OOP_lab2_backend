"""Integration tests for brigade assembly and the work plan."""


def _auth(token):
    return {"Authorization": f"Bearer {token}"}


def _make_request(client, tenant_token, work_type="electrical"):
    return client.post(
        "/api/requests",
        headers=_auth(tenant_token),
        json={
            "tenant_name": "Olena",
            "address": "Shevchenka 1",
            "work_type": work_type,
            "volume_hours": 4,
        },
    ).json()


def _make_specialist(client, dispatcher_token, specialty="electrical"):
    return client.post(
        "/api/specialists",
        headers=_auth(dispatcher_token),
        json={"full_name": "Petro", "specialty": specialty},
    ).json()


def test_create_brigade_assigns_request(client, tenant_token, dispatcher_token):
    request = _make_request(client, tenant_token, "electrical")
    specialist = _make_specialist(client, dispatcher_token, "electrical")

    resp = client.post(
        "/api/brigades",
        headers=_auth(dispatcher_token),
        json={
            "name": "Brigade A",
            "request_id": request["id"],
            "specialist_ids": [specialist["id"]],
            "scheduled_at": "2026-07-01T09:00:00",
        },
    )
    assert resp.status_code == 201
    assert len(resp.json()["specialists"]) == 1

    updated = client.get(
        f"/api/requests/{request['id']}", headers=_auth(tenant_token)
    ).json()
    assert updated["status"] == "assigned"


def test_brigade_rejects_wrong_specialty(client, tenant_token, dispatcher_token):
    request = _make_request(client, tenant_token, "electrical")
    plumber = _make_specialist(client, dispatcher_token, "plumbing")

    resp = client.post(
        "/api/brigades",
        headers=_auth(dispatcher_token),
        json={
            "name": "Bad Brigade",
            "request_id": request["id"],
            "specialist_ids": [plumber["id"]],
        },
    )
    assert resp.status_code == 422


def test_tenant_cannot_create_brigade(client, tenant_token):
    resp = client.post(
        "/api/brigades",
        headers=_auth(tenant_token),
        json={"name": "X", "request_id": 1, "specialist_ids": [1]},
    )
    assert resp.status_code == 403
