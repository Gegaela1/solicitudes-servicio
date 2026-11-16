import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import StaleDataError
from app.db.session import SessionLocal, engine
from app.models.entities import Solicitud, Ciclo, Intervencion, Notificacion
from test_auth import add_user, auth
from test_cases import create_case, finalized


def test_real_optimistic_concurrency(client):
    add_user()
    c = create_case(client, auth(client))
    with SessionLocal() as one, SessionLocal() as two:
        a = one.get(Solicitud, c["id"])
        b = two.get(Solicitud, c["id"])
        a.asunto = "Cambio desde sesión uno"
        one.commit()
        b.asunto = "Cambio desde sesión dos"
        with pytest.raises(StaleDataError):
            two.commit()
    with SessionLocal() as db:
        assert db.get(Solicitud, c["id"]).asunto == "Cambio desde sesión uno"


def test_integrity_foreign_keys_and_rollback(client):
    add_user()
    c = create_case(client, auth(client))
    with SessionLocal() as db:
        before = len(list(db.scalars(select(Intervencion))))
        db.add(
            Intervencion(
                solicitud_id=c["id"], autor_id=99999, tipo="nota", detalle="Autor inexistente"
            )
        )
        with pytest.raises(IntegrityError):
            db.commit()
        db.rollback()
        assert len(list(db.scalars(select(Intervencion)))) == before


def test_rejected_reopening_keeps_result(client):
    h, co, staff, c, cid, aid = finalized(client)
    r = client.post(
        f"/api/v1/solicitudes/{c['id']}/reaperturas",
        headers=h,
        json={"version": c["version"], "motivo": "Solicito estudiar nuevamente este resultado"},
    )
    c = r.json()
    req = client.get(f"/api/v1/solicitudes/{c['id']}/reaperturas", headers=co).json()["items"][0]
    r = client.post(
        f"/api/v1/reaperturas/{req['id']}/decision",
        headers=co,
        json={
            "version": c["version"],
            "aprobar": False,
            "motivo": "Se confirma que la respuesta resuelve el trámite",
        },
    )
    assert r.status_code == 200 and r.json()["estado"] == "finalizada"
    assert (
        client.get(f"/api/v1/solicitudes/{c['id']}/resultado", headers=h).json()["resultado"]
        == "Orientación realizada"
    )
    with SessionLocal() as db:
        assert len(list(db.scalars(select(Ciclo)))) == 1


def test_persistence_new_connection(client):
    add_user()
    c = create_case(client, auth(client))
    engine.dispose()
    with engine.connect() as connection:
        assert (
            connection.scalar(
                text("SELECT radicado FROM solicitudes WHERE id=:id"), {"id": c["id"]}
            )
            == c["radicado"]
        )


def test_other_owner_duplicate_not_allowed(client):
    add_user()
    h = auth(client)
    a = create_case(client, h)
    add_user("otra@example.com")
    b = create_case(client, auth(client, "otra@example.com"))
    add_user("coord@example.com", ("coordinacion",))
    co = auth(client, "coord@example.com")
    r = client.post(
        f"/api/v1/solicitudes/{a['id']}/duplicidad",
        headers=co,
        json={
            "version": a["version"],
            "original_id": b["id"],
            "motivo": "Intento de vincular propietarios distintos",
        },
    )
    assert r.status_code == 422


def test_atomic_action_rolls_back_history_and_notice(client, monkeypatch):
    add_user()
    h = auth(client)
    c = create_case(client, h)
    add_user("staff@example.com", ("atencion",))
    s = auth(client, "staff@example.com")
    import app.services.cases as service

    def fail(db, case, kind, internal):
        raise RuntimeError("Fallo controlado de prueba")

    monkeypatch.setattr(service, "notify", fail)
    with pytest.raises(RuntimeError):
        client.post(
            f"/api/v1/solicitudes/{c['id']}/revision", headers=s, json={"version": c["version"]}
        )
    with SessionLocal() as db:
        assert db.get(Solicitud, c["id"]).estado == "registrada"
        assert len(list(db.scalars(select(Intervencion)))) == 1
        assert (
            len(list(db.scalars(select(Notificacion).where(Notificacion.destinatario_id == 1))))
            == 1
        )
