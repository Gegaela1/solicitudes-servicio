from app.services.notifications import notify
import json
from datetime import timedelta
from fastapi import HTTPException
from sqlalchemy import select
from app.db.session import utcnow
from app.models.entities import Solicitud, Intervencion, Ciclo
from app.services.permissions import can_view

ACTIVE = (
    "registrada",
    "en_revision",
    "pendiente_informacion",
    "aceptada",
    "asignada",
    "en_atencion",
)


def case_by_id(db, user, sid, version=None):
    case = db.get(Solicitud, sid)
    if not case:
        raise HTTPException(404, "Solicitud no encontrada")
    can_view(user, case)
    if version is not None and case.version != version:
        raise HTTPException(409, "El caso cambió. Recarga antes de continuar.")
    return case


def state(case, *allowed):
    if case.estado not in allowed:
        raise HTTPException(409, "La operación no corresponde al estado actual")


def event(db, case, user, kind, detail, internal=False, before=None, changes=None, rectifies=None):
    db.add(
        Intervencion(
            solicitud_id=case.id,
            autor_id=user.id,
            tipo=kind,
            detalle=detail,
            interna=internal,
            estado_anterior=before,
            estado_nuevo=case.estado,
            datos_cambio=json.dumps(changes, ensure_ascii=False, default=str) if changes else None,
            rectifica_id=rectifies,
        )
    )
    case.actualizada_en = utcnow()
    notify(db, case, kind, internal)


def current_cycle(db, case):
    return db.scalar(
        select(Ciclo).where(Ciclo.solicitud_id == case.id).order_by(Ciclo.numero.desc())
    )


def iso(value):
    return value.isoformat() + "Z" if value else None


def case_output(db, case):
    fields = (
        "id",
        "radicado",
        "solicitante_id",
        "servicio_id",
        "responsable_id",
        "nombre",
        "documento",
        "correo",
        "asunto",
        "descripcion",
        "estado",
        "prioridad",
        "plazo_horas",
        "version",
    )
    result = {f: getattr(case, f) for f in fields}
    for f in (
        "creada_en",
        "actualizada_en",
        "revision_iniciada_en",
        "atencion_iniciada_en",
        "finalizada_en",
    ):
        result[f] = iso(getattr(case, f))
    cycle = current_cycle(db, case)
    now = utcnow()
    due = cycle.inicio + timedelta(hours=cycle.plazo_horas) if cycle and cycle.plazo_horas else None
    result.update(
        {
            "vencimiento": iso(due),
            "vencida": bool(due and due < now and case.estado in ACTIVE),
            "duracion_total_horas": (
                (cycle.fin if cycle and case.estado not in ACTIVE and cycle.fin else now)
                - case.creada_en
            ).total_seconds()
            / 3600,
            "duracion_ciclo_horas": ((cycle.fin or now) - cycle.inicio).total_seconds() / 3600
            if cycle
            else None,
        }
    )
    return result


def filtered(db, user, filters):
    from datetime import datetime, time, timezone
    from zoneinfo import ZoneInfo
    from app.services.permissions import is_staff

    q = select(Solicitud)
    if not is_staff(user):
        q = q.where(Solicitud.solicitante_id == user.id)
    for field in ("estado", "responsable_id", "servicio_id", "prioridad", "radicado"):
        value = getattr(filters, field)
        if value is not None:
            q = q.where(getattr(Solicitud, field) == value)
    zone = ZoneInfo("America/Bogota")
    if filters.desde:
        start = (
            datetime.combine(filters.desde, time.min, zone)
            .astimezone(timezone.utc)
            .replace(tzinfo=None)
        )
        q = q.where(Solicitud.creada_en >= start)
    if filters.hasta:
        end = (
            datetime.combine(filters.hasta + timedelta(days=1), time.min, zone)
            .astimezone(timezone.utc)
            .replace(tzinfo=None)
        )
        q = q.where(Solicitud.creada_en < end)
    return q
