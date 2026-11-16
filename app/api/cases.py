from app.schemas.cases import Correction
from app.services.cases import ACTIVE
from app.services.cases import state, iso
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.api.deps import current_user
from app.db.session import get_db, utcnow
from app.models.entities import Solicitud, Servicio, Ciclo
from app.schemas.cases import CaseCreate, Filters
from app.services.cases import filtered, case_by_id, event, case_output
from app.services.permissions import require_roles

router = APIRouter(prefix="/api/v1", tags=["Solicitudes"])


@router.get("/servicios")
def services(user=Depends(current_user), db: Session = Depends(get_db)):
    return [
        {
            "id": s.id,
            "nombre": s.nombre,
            "activo": s.activo,
            "prioridad": s.prioridad,
            "plazo_horas": s.plazo_horas,
        }
        for s in db.scalars(select(Servicio).order_by(Servicio.id))
    ]


@router.post("/solicitudes", status_code=201)
def create(data: CaseCreate, user=Depends(current_user), db: Session = Depends(get_db)):
    require_roles(user, "solicitante")
    service = db.get(Servicio, data.servicio_id)
    if not service or not service.activo:
        raise HTTPException(422, "Servicio inexistente o inactivo")
    case = Solicitud(
        **data.model_dump(mode="json"),
        solicitante_id=user.id,
        prioridad=service.prioridad,
        plazo_horas=service.plazo_horas,
    )
    db.add(case)
    db.flush()
    case.radicado = f"SOL-{utcnow().year}-{case.id:08d}"
    db.add(
        Ciclo(solicitud_id=case.id, numero=1, inicio=case.creada_en, plazo_horas=case.plazo_horas)
    )
    event(db, case, user, "registro", "Solicitud registrada")
    db.commit()
    return case_output(db, case)


@router.get("/solicitudes")
def listing(
    filters: Annotated[Filters, Query()], user=Depends(current_user), db: Session = Depends(get_db)
):
    q = filtered(db, user, filters)
    total = db.scalar(select(func.count()).select_from(q.subquery()))
    items = list(
        db.scalars(
            q.order_by(Solicitud.creada_en.desc(), Solicitud.id.desc())
            .offset((filters.page - 1) * filters.size)
            .limit(filters.size)
        )
    )
    return {
        "items": [case_output(db, c) for c in items],
        "total": total,
        "page": filters.page,
        "size": filters.size,
    }


@router.get("/solicitudes/{sid}")
def detail(sid: int, user=Depends(current_user), db: Session = Depends(get_db)):
    return case_output(db, case_by_id(db, user, sid))


@router.get("/solicitudes/{sid}/resultado")
def result(sid: int, user=Depends(current_user), db: Session = Depends(get_db)):
    case = case_by_id(db, user, sid)
    state(case, "finalizada")
    return {
        "radicado": case.radicado,
        "respuesta": case.respuesta_final,
        "resultado": case.resultado_final,
        "finalizada_en": iso(case.finalizada_en),
    }


@router.patch("/solicitudes/{sid}")
def correct(sid: int, data: Correction, user=Depends(current_user), db: Session = Depends(get_db)):
    case = case_by_id(db, user, sid, data.version)
    personal = case.solicitante_id == user.id and case.estado == "registrada"
    if not personal:
        require_roles(user, "coordinacion")
        state(case, *ACTIVE)
        if not data.motivo:
            raise HTTPException(422, "Corrección administrativa requiere motivo")
    service = db.get(Servicio, data.servicio_id)
    if not service or not service.activo:
        raise HTTPException(422, "Servicio inexistente o inactivo")
    fields = ("nombre", "documento", "correo", "servicio_id", "asunto", "descripcion")
    before = {f: getattr(case, f) for f in fields}
    for f in fields:
        setattr(case, f, getattr(data, f))
    after = {f: getattr(case, f) for f in fields}
    if before == after:
        raise HTTPException(409, "No hay cambios para registrar")
    event(
        db,
        case,
        user,
        "auditoria_correccion",
        data.motivo or "Corrección por propietario",
        internal=True,
        changes={"antes": before, "despues": after},
    )
    event(db, case, user, "correccion", "Datos de la solicitud corregidos")
    db.commit()
    return case_output(db, case)
