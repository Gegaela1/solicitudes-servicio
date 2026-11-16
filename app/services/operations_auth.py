from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.deps import public_user
from app.core.security import DUMMY_HASH, password_hash, token_for, verify_password
from app.models.entities import Usuario, Rol
from app.schemas.common import Login, PasswordChange, Registration


def login(data: Login, db: Session = None):
    user = db.scalar(select(Usuario).where(Usuario.correo == str(data.correo)))
    valid = verify_password(data.contrasena, user.hash_contrasena if user else DUMMY_HASH)
    if not user or not user.activo or (not valid):
        raise HTTPException(401, "Credenciales inválidas")
    return {"access_token": token_for(user), "token_type": "bearer"}


def me(user=None):
    return public_user(user)


def change_password(data: PasswordChange, user=None, db: Session = None):
    if not verify_password(data.actual, user.hash_contrasena):
        raise HTTPException(401, "Credenciales inválidas")
    user.hash_contrasena = password_hash.hash(data.nueva)
    user.auth_version += 1
    db.commit()
    return {"mensaje": "Contraseña cambiada. Inicia sesión nuevamente."}


def register(data: Registration, db: Session = None):
    user = Usuario(
        **data.model_dump(mode="json", exclude={"contrasena"}),
        hash_contrasena=password_hash.hash(data.contrasena),
        roles=[db.scalar(select(Rol).where(Rol.nombre == "solicitante"))],
    )
    if not user.roles[0]:
        raise HTTPException(409, "Prepara primero el catálogo y los roles")
    db.add(user)
    db.commit()
    return public_user(user)
