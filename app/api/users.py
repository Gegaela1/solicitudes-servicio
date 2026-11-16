from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func, text
from sqlalchemy.orm import Session
from app.api.deps import current_user, public_user, roles
from app.core.security import password_hash
from app.db.session import get_db
from app.models.entities import Usuario, Rol, Solicitud
from app.schemas.users import StaffCreate, StaffUpdate
from app.services.permissions import require_roles

router = APIRouter(prefix="/api/v1/usuarios", tags=["Personal"])
ACTIVE = (
    "registrada",
    "en_revision",
    "pendiente_informacion",
    "aceptada",
    "asignada",
    "en_atencion",
)


@router.get("")
def users(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    user=Depends(current_user),
    db: Session = Depends(get_db),
):
    require_roles(user, "coordinacion")
    return {
        "items": [
            public_user(u)
            for u in db.scalars(
                select(Usuario).order_by(Usuario.id).offset((page - 1) * size).limit(size)
            )
        ],
        "total": db.scalar(select(func.count()).select_from(Usuario)),
        "page": page,
        "size": size,
    }


@router.post("", status_code=201)
def create(data: StaffCreate, user=Depends(current_user), db: Session = Depends(get_db)):
    require_roles(user, "coordinacion")
    target = Usuario(
        **data.model_dump(mode="json", exclude={"contrasena", "roles"}),
        hash_contrasena=password_hash.hash(data.contrasena),
        roles=list(db.scalars(select(Rol).where(Rol.nombre.in_(set(data.roles))))),
    )
    db.add(target)
    db.commit()
    return public_user(target)


@router.put("/{uid}/roles")
def update(uid: int, data: StaffUpdate, user=Depends(current_user), db: Session = Depends(get_db)):
    # SQLite reserva la escritura antes de comprobar invariantes globales.
    db.execute(text("BEGIN IMMEDIATE"))
    db.refresh(user)
    require_roles(user, "coordinacion")
    target = db.get(Usuario, uid)
    if not target:
        raise HTTPException(404, "Cuenta no encontrada")
    new_roles = set(data.roles)
    if (
        target.activo
        and "coordinacion" in roles(target)
        and (not data.activo or "coordinacion" not in new_roles)
    ):
        count = db.scalar(
            select(func.count())
            .select_from(Usuario)
            .where(Usuario.activo.is_(True), Usuario.roles.any(Rol.nombre == "coordinacion"))
        )
        if count <= 1:
            raise HTTPException(409, "Debe conservarse al menos una coordinación activa")
    if not data.activo or not new_roles.intersection({"atencion", "coordinacion"}):
        assigned = db.scalar(
            select(func.count())
            .select_from(Solicitud)
            .where(Solicitud.responsable_id == uid, Solicitud.estado.in_(ACTIVE))
        )
        if assigned:
            raise HTTPException(409, "Reasigna primero los casos activos de esta persona")
    target.activo = data.activo
    target.roles = list(db.scalars(select(Rol).where(Rol.nombre.in_(new_roles))))
    target.auth_version += 1
    db.commit()
    return public_user(target)
