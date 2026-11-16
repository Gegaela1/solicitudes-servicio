from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import current_user
from app.db.session import get_db, utcnow
from app.schemas.cases import Action, Motive
from app.services.cases import case_by_id, state, event, case_output, current_cycle
from app.services.permissions import require_roles

router = APIRouter(prefix="/api/v1/solicitudes", tags=["Atención"])


def transition(db, case, user, new, kind, detail):
    before = case.estado
    case.estado = new
    event(db, case, user, kind, detail, before=before)


@router.post("/{sid}/revision")
def review(sid: int, data: Action, user=Depends(current_user), db: Session = Depends(get_db)):
    require_roles(user, "atencion", "coordinacion")
    case = case_by_id(db, user, sid, data.version)
    state(case, "registrada")
    case.revision_iniciada_en = utcnow()
    transition(db, case, user, "en_revision", "revision", "Revisión iniciada")
    db.commit()
    return case_output(db, case)


@router.post("/{sid}/aceptacion")
def accept(sid: int, data: Action, user=Depends(current_user), db: Session = Depends(get_db)):
    require_roles(user, "atencion", "coordinacion")
    case = case_by_id(db, user, sid, data.version)
    state(case, "en_revision")
    transition(db, case, user, "aceptada", "aceptacion", "Solicitud aceptada")
    db.commit()
    return case_output(db, case)


@router.post("/{sid}/rechazo")
def reject(sid: int, data: Motive, user=Depends(current_user), db: Session = Depends(get_db)):
    require_roles(user, "atencion", "coordinacion")
    case = case_by_id(db, user, sid, data.version)
    state(case, "en_revision")
    current_cycle(db, case).fin = utcnow()
    transition(db, case, user, "rechazada", "rechazo", data.motivo)
    db.commit()
    return case_output(db, case)
