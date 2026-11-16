from app.services import operations_auth as operations
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import current_user
from app.db.session import get_db
from app.schemas.common import Login, PasswordChange, Registration

router = APIRouter(prefix="/api/v1", tags=["Cuentas"])


@router.post("/auth/token")
def login(data: Login, db: Session = Depends(get_db)):
    return operations.login(data=data, db=db)


@router.get("/usuarios/me")
def me(user=Depends(current_user)):
    return operations.me(user=user)


@router.post("/usuarios/me/contrasena")
def change_password(
    data: PasswordChange, user=Depends(current_user), db: Session = Depends(get_db)
):
    return operations.change_password(data=data, user=user, db=db)


@router.post("/auth/registro", status_code=201)
def register(data: Registration, db: Session = Depends(get_db)):
    return operations.register(data=data, db=db)
