from datetime import datetime, timedelta, timezone
import jwt
from sqlalchemy import select
from app.core.security import password_hash, settings
from app.db.session import SessionLocal
from app.models.entities import Usuario, Rol


def add_user(email="persona@example.com", roles=("solicitante",)):
    with SessionLocal.begin() as db:
        user = Usuario(
            nombre="Persona Prueba",
            documento="123456",
            correo=email,
            hash_contrasena=password_hash.hash("PruebaSegura-12345"),
            roles=list(db.scalars(select(Rol).where(Rol.nombre.in_(roles)))),
        )
        db.add(user)
        db.flush()
        return user.id


def auth(client, email="persona@example.com"):
    r = client.post(
        "/api/v1/auth/token", json={"correo": email, "contrasena": "PruebaSegura-12345"}
    )
    assert r.status_code == 200, r.text
    return {"Authorization": "Bearer " + r.json()["access_token"]}


def test_jwt_and_password(client):
    add_user()
    h = auth(client)
    assert client.get("/api/v1/usuarios/me", headers=h).status_code == 200
    assert client.get("/api/v1/usuarios/me").status_code == 401
    assert (
        client.get(
            "/api/v1/usuarios/me", headers={"Authorization": h["Authorization"] + "x"}
        ).status_code
        == 401
    )
    expired = jwt.encode(
        {
            "sub": "1",
            "ver": 1,
            "iat": datetime.now(timezone.utc) - timedelta(hours=2),
            "exp": datetime.now(timezone.utc) - timedelta(hours=1),
        },
        settings.secret_key.get_secret_value(),
        algorithm="HS256",
    )
    assert (
        client.get(
            "/api/v1/usuarios/me", headers={"Authorization": "Bearer " + expired}
        ).status_code
        == 401
    )
    assert (
        client.post(
            "/api/v1/usuarios/me/contrasena",
            headers=h,
            json={"actual": "PruebaSegura-12345", "nueva": "OtraSegura-12345"},
        ).status_code
        == 200
    )
    assert client.get("/api/v1/usuarios/me", headers=h).status_code == 401
    invalid = client.post(
        "/api/v1/auth/token", json={"correo": "no", "contrasena": "secreto-no-reflejar"}
    )
    assert invalid.status_code == 422 and "secreto-no-reflejar" not in invalid.text


def test_register_no_privileges(client):
    data = {
        "nombre": "Persona Prueba",
        "documento": "00123",
        "correo": " MAYUS@example.com ",
        "contrasena": "PruebaSegura-12345",
    }
    r = client.post("/api/v1/auth/registro", json=data)
    assert r.status_code == 201, r.text
    assert r.json()["roles"] == ["solicitante"]
    assert r.json()["correo"] == "mayus@example.com"
    assert "hash_contrasena" not in r.text
    assert client.post("/api/v1/auth/registro", json=data).status_code == 409
    data["roles"] = ["coordinacion"]
    assert client.post("/api/v1/auth/registro", json=data).status_code == 422
