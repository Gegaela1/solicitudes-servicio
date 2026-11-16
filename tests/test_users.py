from test_auth import add_user, auth


def test_staff_and_last_coordinator(client):
    cid = add_user("coord@example.com", ("coordinacion",))
    add_user()
    h = auth(client, "coord@example.com")
    assert client.get("/api/v1/usuarios", headers=auth(client)).status_code == 403
    r = client.post(
        "/api/v1/usuarios",
        headers=h,
        json={
            "nombre": "Otra Persona",
            "documento": "1234",
            "correo": "staff@example.com",
            "contrasena": "PruebaSegura-12345",
            "roles": ["atencion", "solicitante"],
        },
    )
    assert r.status_code == 201, r.text
    assert len(r.json()["roles"]) == 2
    assert (
        client.put(
            f"/api/v1/usuarios/{cid}/roles", headers=h, json={"roles": ["atencion"], "activo": True}
        ).status_code
        == 409
    )
    assert (
        client.put(
            f"/api/v1/usuarios/{cid}/roles",
            headers=h,
            json={"roles": ["coordinacion"], "activo": False},
        ).status_code
        == 409
    )

    staff_id = r.json()["id"]
    previous = auth(client, "staff@example.com")
    updated = client.put(
        f"/api/v1/usuarios/{staff_id}/roles",
        headers=h,
        json={"roles": ["atencion", "solicitante"], "activo": False},
    )
    assert updated.status_code == 200
    assert client.get("/api/v1/usuarios/me", headers=previous).status_code == 401
    assert (
        client.post(
            "/api/v1/auth/token",
            json={"correo": "staff@example.com", "contrasena": "PruebaSegura-12345"},
        ).status_code
        == 401
    )
