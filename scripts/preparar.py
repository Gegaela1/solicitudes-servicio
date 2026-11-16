from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.entities import Rol, Servicio

SERVICIOS = [
    "Expedición de certificados",
    "Actualización de información",
    "Solicitudes de documentos",
    "Consultas sobre trámites",
    "Peticiones generales",
]


def seed():
    with SessionLocal.begin() as db:
        for name in ["solicitante", "atencion", "coordinacion"]:
            if not db.scalar(select(Rol).where(Rol.nombre == name)):
                db.add(Rol(nombre=name))
        for name in SERVICIOS:
            if not db.scalar(select(Servicio).where(Servicio.nombre == name)):
                db.add(Servicio(nombre=name))


if __name__ == "__main__":
    seed()
    print("Catálogo y roles preparados; no se crean contraseñas.")
