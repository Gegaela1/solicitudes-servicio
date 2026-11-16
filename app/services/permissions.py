from fastapi import HTTPException
from app.api.deps import roles


def require_roles(user, *allowed):
    if not roles(user).intersection(allowed):
        raise HTTPException(403, "No tienes permiso para esta operación")


def is_staff(user):
    return bool(roles(user).intersection({"atencion", "coordinacion"}))


def can_view(user, case):
    if not is_staff(user) and case.solicitante_id != user.id:
        raise HTTPException(404, "Solicitud no encontrada")


def owner(user, case):
    if case.solicitante_id != user.id:
        raise HTTPException(403, "Solo el propietario puede realizar esta operación")


def responsible(user, case):
    require_roles(user, "atencion", "coordinacion")
    if case.responsable_id != user.id:
        raise HTTPException(403, "Debes ser responsable de este caso")
