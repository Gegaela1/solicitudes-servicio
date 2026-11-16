from app.services import operations_notifications as operations
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api.deps import current_user
from app.db.session import get_db

router = APIRouter(prefix="/api/v1/notificaciones", tags=["Avisos"])


@router.get("")
def listing(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    user=Depends(current_user),
    db: Session = Depends(get_db),
):
    return operations.listing(page=page, size=size, user=user, db=db)


@router.patch("/{nid}/lectura")
def read(nid: int, user=Depends(current_user), db: Session = Depends(get_db)):
    return operations.read(nid=nid, user=user, db=db)
