from typing import Annotated
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.api.deps import current_user
from app.db.session import get_db, utcnow
from app.models.entities import Solicitud, Ciclo
from app.schemas.cases import Filters
from app.services.cases import filtered, case_output, ACTIVE
from app.services.permissions import require_roles

router = APIRouter(prefix="/api/v1/reportes", tags=["Coordinación"])


@router.get("/solicitudes")
def report(
    filters: Annotated[Filters, Query()], user=Depends(current_user), db: Session = Depends(get_db)
):
    require_roles(user, "coordinacion")
    q = filtered(db, user, filters)
    ids = q.with_only_columns(Solicitud.id)
    condition = Solicitud.id.in_(ids)
    total = db.scalar(select(func.count()).select_from(Solicitud).where(condition))
    counts = {}
    for name in ("estado", "servicio_id", "prioridad"):
        col = getattr(Solicitud, name)
        counts[name] = {
            str(k): v
            for k, v in db.execute(select(col, func.count()).where(condition).group_by(col))
        }
    pending = db.scalar(
        select(func.count()).select_from(Solicitud).where(condition, Solicitud.estado.in_(ACTIVE))
    )
    overdue = db.scalar(
        select(func.count())
        .select_from(Ciclo)
        .join(Solicitud, Solicitud.id == Ciclo.solicitud_id)
        .where(
            condition,
            Solicitud.estado.in_(ACTIVE),
            Ciclo.fin.is_(None),
            Ciclo.plazo_horas.is_not(None),
            func.datetime(Ciclo.inicio, func.printf("+%d hours", Ciclo.plazo_horas)) < utcnow(),
        )
    )
    average = db.scalar(
        select(func.avg((func.julianday(Ciclo.fin) - func.julianday(Ciclo.inicio)) * 24))
        .join(Solicitud, Solicitud.id == Ciclo.solicitud_id)
        .where(condition, Ciclo.resuelto.is_(True))
    )
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
        "conteos": counts,
        "pendientes_activos": pending,
        "vencidas": overdue,
        "promedio_resolucion_horas": average,
    }
