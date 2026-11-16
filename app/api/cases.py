from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.deps import current_user
from app.db.session import get_db, utcnow
from app.models.entities import Solicitud, Servicio, Ciclo
from app.schemas.cases import CaseCreate
from app.services.cases import event, case_output
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
