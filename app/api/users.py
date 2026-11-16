from app.services import operations_users as operations
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api.deps import current_user
from app.db.session import get_db
from app.schemas.users import StaffCreate, StaffUpdate

router = APIRouter(prefix="/api/v1/usuarios", tags=["Personal"])


@router.get("")
def users(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    user=Depends(current_user),
    db: Session = Depends(get_db),
):
    return operations.users(page=page, size=size, user=user, db=db)


@router.post("", status_code=201)
def create(data: StaffCreate, user=Depends(current_user), db: Session = Depends(get_db)):
    return operations.create(data=data, user=user, db=db)


@router.put("/{uid}/roles")
def update(uid: int, data: StaffUpdate, user=Depends(current_user), db: Session = Depends(get_db)):
    return operations.update(uid=uid, data=data, user=user, db=db)
