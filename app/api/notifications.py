from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.api.deps import current_user
from app.db.session import get_db, utcnow
from app.models.entities import Notificacion
from app.services.cases import iso

router = APIRouter(prefix="/api/v1/notificaciones", tags=["Avisos"])


@router.get("")
def listing(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    user=Depends(current_user),
    db: Session = Depends(get_db),
):
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


@router.patch("/{nid}/lectura")
def read(nid: int, user=Depends(current_user), db: Session = Depends(get_db)):
    n = db.get(Notificacion, nid)
    if not n or n.destinatario_id != user.id:
        raise HTTPException(404, "Notificación no encontrada")
    if n.leida_en is None:
        n.leida_en = utcnow()
    db.commit()
    return {"id": n.id, "leida_en": iso(n.leida_en)}
