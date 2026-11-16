from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.entities import Usuario
from app.core.security import settings, ALGORITHM

bearer = HTTPBearer(auto_error=False)


def current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
    db: Session = Depends(get_db),
):
    error = HTTPException(
        401, "Autenticación requerida o inválida", headers={"WWW-Authenticate": "Bearer"}
    )
    if not credentials:
        raise error
    try:
        claims = jwt.decode(
            credentials.credentials,
            settings.secret_key.get_secret_value(),
            algorithms=[ALGORITHM],
            options={"require": ["sub", "exp", "iat", "ver"]},
        )
        uid = int(claims["sub"])
        user = db.get(Usuario, uid)
        if not user or not user.activo or claims["ver"] != user.auth_version:
            raise error
        return user
    except (jwt.InvalidTokenError, ValueError, TypeError):
        raise error from None


def roles(user):
    return {r.nombre for r in user.roles}


def public_user(user):
    return {
        "id": user.id,
        "nombre": user.nombre,
        "documento": user.documento,
        "correo": user.correo,
        "activo": user.activo,
        "roles": sorted(roles(user)),
    }
