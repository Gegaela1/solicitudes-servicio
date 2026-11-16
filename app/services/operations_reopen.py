from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.db.session import utcnow
from app.models.entities import Reapertura, Ciclo
from app.schemas.cases import Motive, ReopenDecision
from app.services.cases import case_by_id, state, event, case_output, current_cycle, iso
from app.services.permissions import owner, require_roles
from app.services.operations_workflow import transition


def listing(sid: int, page: int = None, size: int = None, user=None, db: Session = None):
    case_by_id(db, user, sid)
    q = select(Reapertura).where(Reapertura.solicitud_id == sid)
    return {
        "items": [
            {
                "id": r.id,
                "motivo": r.motivo,
                "estado": r.estado,
                "motivo_decision": r.motivo_decision,
                "creado_en": iso(r.creado_en),
                "resuelto_en": iso(r.resuelto_en),
            }
            for r in db.scalars(
                q.order_by(Reapertura.id.desc()).offset((page - 1) * size).limit(size)
            )
        ],
        "total": db.scalar(select(func.count()).select_from(q.subquery())),
        "page": page,
        "size": size,
    }


def request_reopening(sid: int, data: Motive, user=None, db: Session = None):
    case = case_by_id(db, user, sid, data.version)
    owner(user, case)
    state(case, "finalizada")
    if db.scalar(
        select(Reapertura).where(Reapertura.solicitud_id == sid, Reapertura.estado == "pendiente")
    ):
        raise HTTPException(409, "Ya hay una petición pendiente")
    db.add(Reapertura(solicitud_id=sid, solicitante_id=user.id, motivo=data.motivo))
    event(db, case, user, "peticion_reapertura", data.motivo)
    db.commit()
    return case_output(db, case)


def decide(rid: int, data: ReopenDecision, user=None, db: Session = None):
    require_roles(user, "coordinacion")
    req = db.get(Reapertura, rid)
    if not req:
        raise HTTPException(404, "Petición no encontrada")
    case = case_by_id(db, user, req.solicitud_id, data.version)
    state(case, "finalizada")
    if req.estado != "pendiente":
        raise HTTPException(409, "La petición ya fue resuelta")
    req.estado = "aprobada" if data.aprobar else "rechazada"
    req.motivo_decision = data.motivo
    req.resuelto_por_id = user.id
    req.resuelto_en = utcnow()
    if data.aprobar:
        cycle = current_cycle(db, case)
        previous = {
            "respuesta": case.respuesta_final,
            "resultado": case.resultado_final,
            "finalizada_en": iso(case.finalizada_en),
            "ciclo": cycle.numero,
        }
        event(
            db,
            case,
            user,
            "cierre_ciclo_anterior",
            case.respuesta_final + "\nResultado: " + case.resultado_final,
            changes=previous,
        )
        db.add(
            Ciclo(
                solicitud_id=case.id,
                numero=cycle.numero + 1,
                inicio=utcnow(),
                plazo_horas=case.plazo_horas,
            )
        )
        case.responsable_id = None
        case.respuesta_final = None
        case.resultado_final = None
        case.finalizada_en = None
        case.revision_iniciada_en = utcnow()
        case.atencion_iniciada_en = None
        transition(db, case, user, "en_revision", "reapertura_aprobada", data.motivo)
    else:
        event(db, case, user, "reapertura_rechazada", data.motivo)
    db.commit()
    return case_output(db, case)
