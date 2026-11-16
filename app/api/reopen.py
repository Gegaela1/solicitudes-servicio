from app.services import operations_reopen as operations
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api.deps import current_user
from app.db.session import get_db
from app.schemas.cases import Motive, ReopenDecision

router = APIRouter(prefix="/api/v1", tags=["Reaperturas"])


@router.get("/solicitudes/{sid}/reaperturas")
def listing(
    sid: int,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    user=Depends(current_user),
    db: Session = Depends(get_db),
):
    return operations.listing(sid=sid, page=page, size=size, user=user, db=db)


@router.post("/solicitudes/{sid}/reaperturas", status_code=201)
def request_reopening(
    sid: int, data: Motive, user=Depends(current_user), db: Session = Depends(get_db)
):
    return operations.request_reopening(sid=sid, data=data, user=user, db=db)


@router.post("/reaperturas/{rid}/decision")
def decide(
    rid: int, data: ReopenDecision, user=Depends(current_user), db: Session = Depends(get_db)
):
    return operations.decide(rid=rid, data=data, user=user, db=db)
