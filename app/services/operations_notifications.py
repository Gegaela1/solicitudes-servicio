from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.db.session import utcnow
from app.models.entities import Notificacion
from app.services.cases import iso


def listing(page: int = None, size: int = None, user=None, db: Session = None):
    q = select(Notificacion).where(Notificacion.destinatario_id == user.id)
    return {
        "items": [
            {
                "id": n.id,
                "solicitud_id": n.solicitud_id,
                "mensaje": n.mensaje,
                "creada_en": iso(n.creada_en),
                "leida_en": iso(n.leida_en),
            }
            for n in db.scalars(
                q.order_by(Notificacion.creada_en.desc(), Notificacion.id.desc())
                .offset((page - 1) * size)
                .limit(size)
            )
        ],
        "total": db.scalar(select(func.count()).select_from(q.subquery())),
        "page": page,
        "size": size,
    }


def read(nid: int, user=None, db: Session = None):
    n = db.get(Notificacion, nid)
    if not n or n.destinatario_id != user.id:
        raise HTTPException(404, "Notificación no encontrada")
    if n.leida_en is None:
        n.leida_en = utcnow()
    db.commit()
    return {"id": n.id, "leida_en": iso(n.leida_en)}
