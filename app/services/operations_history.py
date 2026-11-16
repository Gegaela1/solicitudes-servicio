from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.api.deps import roles
from app.models.entities import Intervencion
from app.schemas.cases import Note
from app.services.cases import case_by_id, event, state, ACTIVE, case_output, iso
from app.services.permissions import is_staff, responsible


def history(sid: int, page: int = None, size: int = None, user=None, db: Session = None):
    case_by_id(db, user, sid)
    q = select(Intervencion).where(Intervencion.solicitud_id == sid)
    if not is_staff(user):
        q = q.where(Intervencion.interna.is_(False))
    total = db.scalar(select(func.count()).select_from(q.subquery()))
    items = []
    for i in db.scalars(
        q.order_by(Intervencion.creada_en.desc(), Intervencion.id.desc())
        .offset((page - 1) * size)
        .limit(size)
    ):
        item = {
            "id": i.id,
            "tipo": i.tipo,
            "detalle": i.detalle,
            "creada_en": iso(i.creada_en),
            "estado_anterior": i.estado_anterior,
            "estado_nuevo": i.estado_nuevo,
            "rectifica_id": i.rectifica_id,
        }
        if is_staff(user):
            item.update(
                {"autor_id": i.autor_id, "interna": i.interna, "datos_cambio": i.datos_cambio}
            )
        items.append(item)
    return {"items": items, "total": total, "page": page, "size": size}


def note(sid: int, data: Note, user=None, db: Session = None):
    case = case_by_id(db, user, sid, data.version)
    state(case, *ACTIVE)
    if "coordinacion" not in roles(user):
        responsible(user, case)
    if data.rectifica_id:
        previous = db.get(Intervencion, data.rectifica_id)
        if not previous or previous.solicitud_id != sid:
            raise HTTPException(422, "Intervención ajena o inexistente")
        if previous.tipo not in ("nota", "rectificacion"):
            raise HTTPException(
                409, "Solo se rectifican notas; las acciones tienen su operación específica"
            )
        if previous.interna and (not data.interna):
            raise HTTPException(422, "La rectificación debe conservar visibilidad interna")
    event(
        db,
        case,
        user,
        "rectificacion" if data.rectifica_id else "nota",
        data.detalle,
        internal=data.interna,
        rectifies=data.rectifica_id,
    )
    db.commit()
    return case_output(db, case)
