from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.db.session import utcnow
from app.models.entities import Requerimiento
from app.schemas.cases import Question, Answer
from app.services.cases import case_by_id, state, case_output, iso
from app.services.permissions import require_roles, responsible, owner
from app.services.operations_workflow import transition


def questions(sid: int, page: int = None, size: int = None, user=None, db: Session = None):
    case_by_id(db, user, sid)
    q = select(Requerimiento).where(Requerimiento.solicitud_id == sid)
    return {
        "items": [
            {
                "id": r.id,
                "pregunta": r.pregunta,
                "respuesta": r.respuesta,
                "creado_en": iso(r.creado_en),
                "cerrado_en": iso(r.cerrado_en),
            }
            for r in db.scalars(
                q.order_by(Requerimiento.id.desc()).offset((page - 1) * size).limit(size)
            )
        ],
        "total": db.scalar(select(func.count()).select_from(q.subquery())),
        "page": page,
        "size": size,
    }


def ask(sid: int, data: Question, user=None, db: Session = None):
    case = case_by_id(db, user, sid, data.version)
    state(case, "en_revision", "en_atencion")
    if case.estado == "en_revision":
        require_roles(user, "atencion", "coordinacion")
    else:
        responsible(user, case)
    if db.scalar(
        select(Requerimiento).where(
            Requerimiento.solicitud_id == sid, Requerimiento.cerrado_en.is_(None)
        )
    ):
        raise HTTPException(409, "Ya hay un requerimiento abierto")
    db.add(
        Requerimiento(
            solicitud_id=sid,
            solicitado_por_id=user.id,
            pregunta=data.pregunta,
            etapa_retorno=case.estado,
        )
    )
    transition(db, case, user, "pendiente_informacion", "requerimiento", data.pregunta)
    db.commit()
    return case_output(db, case)


def answer(rid: int, data: Answer, user=None, db: Session = None):
    req = db.get(Requerimiento, rid)
    if not req:
        raise HTTPException(404, "Requerimiento no encontrado")
    case = case_by_id(db, user, req.solicitud_id, data.version)
    owner(user, case)
    state(case, "pendiente_informacion")
    if req.cerrado_en:
        raise HTTPException(409, "El requerimiento ya está cerrado")
    req.respuesta = data.respuesta
    req.respondido_por_id = user.id
    req.respondido_en = utcnow()
    req.cerrado_en = req.respondido_en
    transition(db, case, user, req.etapa_retorno, "respuesta_informacion", data.respuesta)
    db.commit()
    return case_output(db, case)
