from sqlalchemy import select, func
from app.db.session import SessionLocal
from app.models.entities import Solicitud, Intervencion
from test_auth import add_user, auth

CASE = {
    "nombre": "Persona Prueba",
    "documento": "00123",
    "correo": "persona@example.com",
    "servicio_id": 1,
    "asunto": "Consulta administrativa",
    "descripcion": "Necesito información sobre el trámite administrativo.",
}


def create_case(client, h):
    r = client.post("/api/v1/solicitudes", headers=h, json=CASE)
    assert r.status_code == 201, r.text
    return r.json()


def test_persist_valid_and_invalid(client):
    uid = add_user()
    h = auth(client)
    c = create_case(client, h)
    assert c["radicado"].startswith("SOL-") and c["estado"] == "registrada"
    with SessionLocal() as db:
        case = db.get(Solicitud, c["id"])
        assert case.solicitante_id == uid
        assert db.scalar(select(func.count()).select_from(Intervencion)) == 1
    assert (
        client.post(
            "/api/v1/solicitudes", headers=h, json={**CASE, "descripcion": "corta"}
        ).status_code
        == 422
    )
    assert (
        client.post(
            "/api/v1/solicitudes", headers=h, json={**CASE, "solicitante_id": 99}
        ).status_code
        == 422
    )
    with SessionLocal() as db:
        assert db.scalar(select(func.count()).select_from(Solicitud)) == 1
