from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.deps import current_user, public_user
from app.core.security import DUMMY_HASH, password_hash, token_for, verify_password
from app.db.session import get_db
from app.models.entities import Usuario
from app.schemas.common import Login, PasswordChange

router = APIRouter(prefix="/api/v1", tags=["Cuentas"])


@router.post("/auth/token")
def login(data: Login, db: Session = Depends(get_db)):
    user = db.scalar(select(Usuario).where(Usuario.correo == str(data.correo)))
    valid = verify_password(data.contrasena, user.hash_contrasena if user else DUMMY_HASH)
    if not user or not user.activo or not valid:
        raise HTTPException(401, "Credenciales inválidas")
    return {"access_token": token_for(user), "token_type": "bearer"}


@router.get("/usuarios/me")
def me(user=Depends(current_user)):
    return public_user(user)


@router.post("/usuarios/me/contrasena")
def change_password(
    data: PasswordChange, user=Depends(current_user), db: Session = Depends(get_db)
):
    if not verify_password(data.actual, user.hash_contrasena):
        raise HTTPException(401, "Credenciales inválidas")
    user.hash_contrasena = password_hash.hash(data.nueva)
    user.auth_version += 1
    db.commit()
    return {"mensaje": "Contraseña cambiada. Inicia sesión nuevamente."}
