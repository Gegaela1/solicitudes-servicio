from app.services import operations_history as operations
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api.deps import current_user
from app.db.session import get_db
from app.schemas.cases import Note

router = APIRouter(prefix="/api/v1/solicitudes", tags=["Historial"])


@router.get("/{sid}/historial")
def history(
    sid: int,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    user=Depends(current_user),
    db: Session = Depends(get_db),
):
    return operations.history(sid=sid, page=page, size=size, user=user, db=db)


@router.post("/{sid}/intervenciones", status_code=201)
def note(sid: int, data: Note, user=Depends(current_user), db: Session = Depends(get_db)):
    return operations.note(sid=sid, data=data, user=user, db=db)
