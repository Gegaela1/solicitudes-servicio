from app.services.permissions import owner
from app.services.permissions import responsible
from app.schemas.cases import Finalize
from fastapi import HTTPException
from app.models.entities import Usuario
from app.api.deps import roles
from app.services.cases import ACTIVE
from app.schemas.cases import Assign
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


@router.put("/{sid}/responsable")
def assign(sid: int, data: Assign, user=Depends(current_user), db: Session = Depends(get_db)):
    require_roles(user, "coordinacion")
    case = case_by_id(db, user, sid, data.version)
    state(case, *ACTIVE)
    if not case.responsable_id:
        state(case, "aceptada")
    target = db.get(Usuario, data.responsable_id)
    if (
        not target
        or not target.activo
        or not roles(target).intersection({"atencion", "coordinacion"})
    ):
        raise HTTPException(422, "Responsable no elegible")
    if case.responsable_id == target.id:
        raise HTTPException(409, "La persona ya es responsable")
    previous = case.responsable_id
    before = case.estado
    case.responsable_id = target.id
    if previous is None:
        case.estado = "asignada"
    event(
        db,
        case,
        user,
        "asignacion",
        data.motivo,
        internal=True,
        before=before,
        changes={"responsable_anterior": previous, "responsable_nuevo": target.id},
    )
    if before != case.estado:
        event(db, case, user, "estado", "Responsable asignado; solicitud asignada", before=before)
    db.commit()
    return case_output(db, case)


@router.post("/{sid}/inicio-atencion")
def start(sid: int, data: Action, user=Depends(current_user), db: Session = Depends(get_db)):
    case = case_by_id(db, user, sid, data.version)
    responsible(user, case)
    state(case, "asignada")
    case.atencion_iniciada_en = utcnow()
    transition(db, case, user, "en_atencion", "inicio_atencion", "Atención iniciada")
    db.commit()
    return case_output(db, case)


@router.post("/{sid}/finalizacion")
def finish(sid: int, data: Finalize, user=Depends(current_user), db: Session = Depends(get_db)):
    case = case_by_id(db, user, sid, data.version)
    responsible(user, case)
    state(case, "en_atencion")
    case.respuesta_final = data.respuesta
    case.resultado_final = data.resultado
    case.finalizada_en = utcnow()
    cycle = current_cycle(db, case)
    cycle.fin = case.finalizada_en
    cycle.respuesta = data.respuesta
    cycle.resultado = data.resultado
    cycle.resuelto = True
    transition(
        db,
        case,
        user,
        "finalizada",
        "finalizacion",
        data.respuesta + "\nResultado: " + data.resultado,
    )
    db.commit()
    return case_output(db, case)


@router.post("/{sid}/cancelacion")
def cancel(sid: int, data: Motive, user=Depends(current_user), db: Session = Depends(get_db)):
    case = case_by_id(db, user, sid, data.version)
    owner(user, case)
    state(case, "registrada")
    current_cycle(db, case).fin = utcnow()
    transition(db, case, user, "cancelada", "cancelacion", data.motivo)
    db.commit()
    return case_output(db, case)
