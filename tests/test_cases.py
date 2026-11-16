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


def test_visibility_pagination_and_filters(client):
    add_user()
    h = auth(client)
    c = create_case(client, h)
    add_user("otra@example.com")
    other = auth(client, "otra@example.com")
    assert client.get(f"/api/v1/solicitudes/{c['id']}", headers=other).status_code == 404
    assert client.get("/api/v1/solicitudes/99999", headers=h).status_code == 404
    assert client.get("/api/v1/solicitudes", headers=other).json()["total"] == 0
    assert client.get("/api/v1/solicitudes?estado=inventado", headers=h).status_code == 422
    assert client.get("/api/v1/solicitudes?size=101", headers=h).status_code == 422
    assert (
        client.get("/api/v1/solicitudes?desde=2026-11-17&hasta=2026-11-16", headers=h).status_code
        == 422
    )
    assert (
        client.get("/api/v1/solicitudes?radicado=" + c["radicado"], headers=h).json()["total"] == 1
    )


def test_internal_history_and_rectification(client):
    add_user()
    h = auth(client)
    c = create_case(client, h)
    add_user("coord@example.com", ("coordinacion",))
    co = auth(client, "coord@example.com")
    note = client.post(
        f"/api/v1/solicitudes/{c['id']}/intervenciones",
        headers=co,
        json={"version": c["version"], "detalle": "Nota privada", "interna": True},
    )
    assert note.status_code == 201, note.text
    public = client.get(f"/api/v1/solicitudes/{c['id']}/historial", headers=h)
    assert "Nota privada" not in public.text and "datos_cambio" not in public.text
    internal = client.get(f"/api/v1/solicitudes/{c['id']}/historial", headers=co).json()["items"][0]
    assert internal["interna"]
    corrected = client.post(
        f"/api/v1/solicitudes/{c['id']}/intervenciones",
        headers=co,
        json={
            "version": note.json()["version"],
            "detalle": "Nota corregida",
            "interna": True,
            "rectifica_id": internal["id"],
        },
    )
    assert corrected.status_code == 201
    assert client.get(f"/api/v1/solicitudes/{c['id']}/historial", headers=co).json()["total"] == 3


def test_review_states_and_stale_version(client):
    add_user()
    h = auth(client)
    c = create_case(client, h)
    add_user("staff@example.com", ("atencion",))
    s = auth(client, "staff@example.com")
    path = f"/api/v1/solicitudes/{c['id']}"
    assert (
        client.post(path + "/revision", headers=h, json={"version": c["version"]}).status_code
        == 403
    )
    assert (
        client.post(path + "/aceptacion", headers=s, json={"version": c["version"]}).status_code
        == 409
    )
    r = client.post(path + "/revision", headers=s, json={"version": c["version"]})
    assert r.status_code == 200 and r.json()["estado"] == "en_revision"
    assert (
        client.post(path + "/aceptacion", headers=s, json={"version": c["version"]}).status_code
        == 409
    )
    assert (
        client.post(
            path + "/rechazo",
            headers=s,
            json={"version": r.json()["version"], "motivo": "No corresponde a nuestra competencia"},
        ).json()["estado"]
        == "rechazada"
    )


def advance(client, h, c, action, data=None, method="post"):
    r = getattr(client, method)(
        f"/api/v1/solicitudes/{c['id']}/{action}",
        headers=h,
        json={"version": c["version"], **(data or {})},
    )
    assert r.status_code == 200, r.text
    return r.json()


def prepared(client):
    add_user()
    h = auth(client)
    cid = add_user("coord@example.com", ("coordinacion",))
    co = auth(client, "coord@example.com")
    aid = add_user("staff@example.com", ("atencion",))
    staff = auth(client, "staff@example.com")
    c = create_case(client, h)
    c = advance(client, staff, c, "revision")
    c = advance(client, staff, c, "aceptacion")
    return h, co, staff, c, cid, aid


def test_assign_and_active_responsible(client):
    h, co, staff, c, cid, aid = prepared(client)
    path = f"/api/v1/solicitudes/{c['id']}/responsable"
    assert (
        client.put(
            path,
            headers=staff,
            json={
                "version": c["version"],
                "responsable_id": aid,
                "motivo": "Asignación inicial válida",
            },
        ).status_code
        == 403
    )
    assert (
        client.put(
            path,
            headers=co,
            json={
                "version": c["version"],
                "responsable_id": 9999,
                "motivo": "Asignación inicial válida",
            },
        ).status_code
        == 422
    )
    c = advance(
        client,
        co,
        c,
        "responsable",
        {"responsable_id": aid, "motivo": "Asignación inicial válida"},
        "put",
    )
    assert c["estado"] == "asignada"
    assert (
        client.put(
            f"/api/v1/usuarios/{aid}/roles",
            headers=co,
            json={"roles": ["solicitante"], "activo": True},
        ).status_code
        == 409
    )
    c = advance(
        client,
        co,
        c,
        "responsable",
        {"responsable_id": cid, "motivo": "Cambio por disponibilidad"},
        "put",
    )
    assert c["estado"] == "asignada" and c["responsable_id"] == cid


def finalized(client):
    h, co, staff, c, cid, aid = prepared(client)
    c = advance(
        client,
        co,
        c,
        "responsable",
        {"responsable_id": aid, "motivo": "Asignación para resolución"},
        "put",
    )
    c = advance(client, staff, c, "inicio-atencion")
    c = advance(
        client,
        staff,
        c,
        "finalizacion",
        {"respuesta": "Respuesta del trámite completado", "resultado": "Orientación realizada"},
    )
    return h, co, staff, c, cid, aid


def test_finish_requires_assigned_actor(client):
    h, co, staff, c, cid, aid = prepared(client)
    c = advance(
        client,
        co,
        c,
        "responsable",
        {"responsable_id": aid, "motivo": "Asignación para resolución"},
        "put",
    )
    path = f"/api/v1/solicitudes/{c['id']}"
    assert (
        client.post(
            path + "/inicio-atencion", headers=co, json={"version": c["version"]}
        ).status_code
        == 403
    )
    c = advance(client, staff, c, "inicio-atencion")
    assert (
        client.post(
            path + "/finalizacion",
            headers=staff,
            json={"version": c["version"], "respuesta": "corta", "resultado": "hecho"},
        ).status_code
        == 422
    )
    c = advance(
        client,
        staff,
        c,
        "finalizacion",
        {"respuesta": "Respuesta del trámite completado", "resultado": "Orientación realizada"},
    )
    assert c["estado"] == "finalizada"
    from app.models.entities import Ciclo

    with SessionLocal() as db:
        cycle = db.scalar(select(Ciclo).where(Ciclo.solicitud_id == c["id"]))
        assert cycle.resuelto and cycle.resultado == "Orientación realizada"


def test_owner_result_and_history(client):
    h, co, staff, c, cid, aid = finalized(client)
    result = client.get(f"/api/v1/solicitudes/{c['id']}/resultado", headers=h)
    assert result.status_code == 200 and result.json()["resultado"] == "Orientación realizada"
    history = client.get(f"/api/v1/solicitudes/{c['id']}/historial", headers=h)
    assert any(i["tipo"] == "finalizacion" for i in history.json()["items"])
    add_user("otro@example.com")
    assert (
        client.get(
            f"/api/v1/solicitudes/{c['id']}/resultado", headers=auth(client, "otro@example.com")
        ).status_code
        == 404
    )


def test_information_roundtrip(client):
    add_user()
    h = auth(client)
    c = create_case(client, h)
    add_user("staff@example.com", ("atencion",))
    s = auth(client, "staff@example.com")
    c = advance(client, s, c, "revision")
    r = client.post(
        f"/api/v1/solicitudes/{c['id']}/requerimientos",
        headers=s,
        json={
            "version": c["version"],
            "pregunta": "Por favor precisa cuál es el trámite solicitado",
        },
    )
    assert r.status_code == 201, r.text
    c = r.json()
    assert c["estado"] == "pendiente_informacion"
    assert (
        client.post(
            f"/api/v1/solicitudes/{c['id']}/requerimientos",
            headers=s,
            json={"version": c["version"], "pregunta": "Otra pregunta adicional"},
        ).status_code
        == 409
    )
    req = client.get(f"/api/v1/solicitudes/{c['id']}/requerimientos", headers=h).json()["items"][0]
    r = client.post(
        f"/api/v1/requerimientos/{req['id']}/respuesta",
        headers=h,
        json={"version": c["version"], "respuesta": "Solicito orientación administrativa"},
    )
    assert r.status_code == 200 and r.json()["estado"] == "en_revision"
    assert (
        client.post(
            f"/api/v1/requerimientos/{req['id']}/respuesta",
            headers=h,
            json={"version": r.json()["version"], "respuesta": "otra"},
        ).status_code
        == 409
    )


def test_correction_limits(client):
    add_user()
    h = auth(client)
    c = create_case(client, h)
    changed = {**CASE, "asunto": "Asunto corregido", "version": c["version"]}
    r = client.patch(f"/api/v1/solicitudes/{c['id']}", headers=h, json=changed)
    assert r.status_code == 200, r.text
    c = r.json()
    add_user("staff@example.com", ("atencion",))
    s = auth(client, "staff@example.com")
    c = advance(client, s, c, "revision")
    changed.update(version=c["version"], asunto="Segunda corrección")
    assert (
        client.patch(f"/api/v1/solicitudes/{c['id']}", headers=h, json=changed).status_code == 403
    )
    add_user("coord@example.com", ("coordinacion",))
    co = auth(client, "coord@example.com")
    assert (
        client.patch(f"/api/v1/solicitudes/{c['id']}", headers=co, json=changed).status_code == 422
    )
    changed["motivo"] = "Corrección administrativa justificada"
    assert (
        client.patch(f"/api/v1/solicitudes/{c['id']}", headers=co, json=changed).status_code == 200
    )


def test_cancel_before_review_only(client):
    add_user()
    h = auth(client)
    c = create_case(client, h)
    c = advance(client, h, c, "cancelacion", {"motivo": "La solicitud ya no es necesaria"})
    assert c["estado"] == "cancelada"
    assert (
        client.post(
            f"/api/v1/solicitudes/{c['id']}/cancelacion",
            headers=h,
            json={"version": c["version"], "motivo": "Intento repetido de cancelación"},
        ).status_code
        == 409
    )
    c = create_case(client, h)
    add_user("staff@example.com", ("atencion",))
    s = auth(client, "staff@example.com")
    c = advance(client, s, c, "revision")
    assert (
        client.post(
            f"/api/v1/solicitudes/{c['id']}/cancelacion",
            headers=h,
            json={"version": c["version"], "motivo": "Quiero cancelar la solicitud"},
        ).status_code
        == 409
    )


def test_reopen_preserves_finalized_cycle(client):
    h, co, staff, c, cid, aid = finalized(client)
    rad = c["radicado"]
    r = client.post(
        f"/api/v1/solicitudes/{c['id']}/reaperturas",
        headers=h,
        json={"version": c["version"], "motivo": "La respuesta requiere una aclaración adicional"},
    )
    assert r.status_code == 201 and r.json()["estado"] == "finalizada"
    c = r.json()
    assert (
        client.post(
            f"/api/v1/solicitudes/{c['id']}/reaperturas",
            headers=h,
            json={"version": c["version"], "motivo": "Otra solicitud de reapertura"},
        ).status_code
        == 409
    )
    req = client.get(f"/api/v1/solicitudes/{c['id']}/reaperturas", headers=co).json()["items"][0]
    r = client.post(
        f"/api/v1/reaperturas/{req['id']}/decision",
        headers=co,
        json={
            "version": c["version"],
            "aprobar": True,
            "motivo": "Se aprueba estudiar la información adicional",
        },
    )
    assert r.status_code == 200, r.text
    c = r.json()
    assert c["estado"] == "en_revision" and c["radicado"] == rad and c["responsable_id"] is None
    from app.models.entities import Ciclo

    with SessionLocal() as db:
        cycles = list(
            db.scalars(select(Ciclo).where(Ciclo.solicitud_id == c["id"]).order_by(Ciclo.numero))
        )
        assert (
            len(cycles) == 2
            and cycles[0].respuesta
            and cycles[0].resuelto
            and cycles[1].fin is None
        )
        assert db.get(Solicitud, c["id"]).respuesta_final is None
    history = client.get(f"/api/v1/solicitudes/{c['id']}/historial", headers=h).text
    assert "Respuesta del trámite completado" in history


def test_duplicates_preserve_history_and_close_question(client):
    add_user()
    h = auth(client)
    original = create_case(client, h)
    c = create_case(client, h)
    add_user("coord@example.com", ("coordinacion",))
    co = auth(client, "coord@example.com")
    c = advance(client, co, c, "revision")
    r = client.post(
        f"/api/v1/solicitudes/{c['id']}/requerimientos",
        headers=co,
        json={"version": c["version"], "pregunta": "Precisa el alcance de esta solicitud"},
    )
    c = r.json()
    assert (
        client.post(
            f"/api/v1/solicitudes/{c['id']}/duplicidad",
            headers=co,
            json={
                "version": c["version"],
                "original_id": c["id"],
                "motivo": "Caso duplicado por revisión manual",
            },
        ).status_code
        == 422
    )
    c = advance(
        client,
        co,
        c,
        "duplicidad",
        {"original_id": original["id"], "motivo": "Caso duplicado por revisión manual"},
    )
    assert c["estado"] == "cerrada_duplicidad"
    req = client.get(f"/api/v1/solicitudes/{c['id']}/requerimientos", headers=h).json()["items"][0]
    assert req["cerrado_en"]
    # No se puede usar un duplicado como original, lo que también impide ciclos.
    assert (
        client.post(
            f"/api/v1/solicitudes/{original['id']}/duplicidad",
            headers=co,
            json={
                "version": original["version"],
                "original_id": c["id"],
                "motivo": "Intento de relación circular",
            },
        ).status_code
        == 422
    )
    assert client.get(f"/api/v1/solicitudes/{c['id']}/historial", headers=h).json()["total"] >= 4


def test_service_snapshots_deadline(client):
    from datetime import timedelta
    from app.models.entities import Ciclo
    from app.db.session import utcnow

    add_user()
    h = auth(client)
    add_user("coord@example.com", ("coordinacion",))
    co = auth(client, "coord@example.com")
    old = create_case(client, h)
    assert old["vencimiento"] is None
    assert (
        client.patch(
            "/api/v1/servicios/1/configuracion",
            headers=co,
            json={"prioridad": "alta", "plazo_horas": 0},
        ).status_code
        == 422
    )
    assert (
        client.patch(
            "/api/v1/servicios/1/configuracion",
            headers=co,
            json={"prioridad": "alta", "plazo_horas": 24},
        ).status_code
        == 200
    )
    c = create_case(client, h)
    assert c["prioridad"] == "alta" and c["vencimiento"]
    assert client.get(f"/api/v1/solicitudes/{old['id']}", headers=h).json()["plazo_horas"] is None
    with SessionLocal.begin() as db:
        cycle = db.scalar(select(Ciclo).where(Ciclo.solicitud_id == c["id"]))
        cycle.inicio = utcnow() - timedelta(hours=25)
    assert client.get(f"/api/v1/solicitudes/{c['id']}", headers=h).json()["vencida"] is True
