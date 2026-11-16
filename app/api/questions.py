from app.services import operations_questions as operations
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api.deps import current_user
from app.db.session import get_db
from app.schemas.cases import Question, Answer

router = APIRouter(prefix="/api/v1", tags=["Información adicional"])


@router.get("/solicitudes/{sid}/requerimientos")
def questions(
    sid: int,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    user=Depends(current_user),
    db: Session = Depends(get_db),
):
    return operations.questions(sid=sid, page=page, size=size, user=user, db=db)


@router.post("/solicitudes/{sid}/requerimientos", status_code=201)
def ask(sid: int, data: Question, user=Depends(current_user), db: Session = Depends(get_db)):
    return operations.ask(sid=sid, data=data, user=user, db=db)


@router.post("/requerimientos/{rid}/respuesta")
def answer(rid: int, data: Answer, user=Depends(current_user), db: Session = Depends(get_db)):
    return operations.answer(rid=rid, data=data, user=user, db=db)
