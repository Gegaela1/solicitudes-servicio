from app.services import operations_workflow as operations
from app.schemas.cases import Duplicate
from app.schemas.cases import Finalize
from app.schemas.cases import Assign
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import current_user
from app.db.session import get_db
from app.schemas.cases import Action, Motive

router = APIRouter(prefix="/api/v1/solicitudes", tags=["Atención"])


@router.post("/{sid}/revision")
def review(sid: int, data: Action, user=Depends(current_user), db: Session = Depends(get_db)):
    return operations.review(sid=sid, data=data, user=user, db=db)


@router.post("/{sid}/aceptacion")
def accept(sid: int, data: Action, user=Depends(current_user), db: Session = Depends(get_db)):
    return operations.accept(sid=sid, data=data, user=user, db=db)


@router.post("/{sid}/rechazo")
def reject(sid: int, data: Motive, user=Depends(current_user), db: Session = Depends(get_db)):
    return operations.reject(sid=sid, data=data, user=user, db=db)


@router.put("/{sid}/responsable")
def assign(sid: int, data: Assign, user=Depends(current_user), db: Session = Depends(get_db)):
    return operations.assign(sid=sid, data=data, user=user, db=db)


@router.post("/{sid}/inicio-atencion")
def start(sid: int, data: Action, user=Depends(current_user), db: Session = Depends(get_db)):
    return operations.start(sid=sid, data=data, user=user, db=db)


@router.post("/{sid}/finalizacion")
def finish(sid: int, data: Finalize, user=Depends(current_user), db: Session = Depends(get_db)):
    return operations.finish(sid=sid, data=data, user=user, db=db)


@router.post("/{sid}/cancelacion")
def cancel(sid: int, data: Motive, user=Depends(current_user), db: Session = Depends(get_db)):
    return operations.cancel(sid=sid, data=data, user=user, db=db)


@router.post("/{sid}/duplicidad")
def duplicate(sid: int, data: Duplicate, user=Depends(current_user), db: Session = Depends(get_db)):
    return operations.duplicate(sid=sid, data=data, user=user, db=db)
