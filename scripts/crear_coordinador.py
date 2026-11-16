from sqlalchemy.exc import IntegrityError
from getpass import getpass
from sqlalchemy import select, func
from app.db.session import SessionLocal
from app.models.entities import Usuario, Rol
from app.schemas.common import Identity, Password
from pydantic import TypeAdapter, ValidationError
from app.core.security import password_hash
from scripts.preparar import seed


def create_initial():
    seed()
    with SessionLocal.begin() as db:
        count = db.scalar(
            select(func.count())
            .select_from(Usuario)
            .where(Usuario.activo.is_(True), Usuario.roles.any(Rol.nombre == "coordinacion"))
        )
        if count:
            print("Ya existe coordinación activa. Utiliza la administración del sistema.")
            return
        try:
            data = Identity(
                nombre=input("Nombre: "), documento=input("Documento: "), correo=input("Correo: ")
            )
            password = TypeAdapter(Password).validate_python(
                getpass("Contraseña (mínimo 12 caracteres): ")
            )
            if password != getpass("Repite la contraseña: "):
                print("Las contraseñas no coinciden. No se creó la cuenta.")
                return
        except ValidationError:
            print("Datos inválidos. Revisa las longitudes y el correo; no se creó la cuenta.")
            return
        db.add(
            Usuario(
                **data.model_dump(mode="json"),
                hash_contrasena=password_hash.hash(password),
                roles=[db.scalar(select(Rol).where(Rol.nombre == "coordinacion"))],
            )
        )
    print("Coordinación creada; inicia sesión en la aplicación.")


def main():
    try:
        create_initial()
    except IntegrityError:
        print(
            "No se creó la cuenta: el correo ya existe o cambió la configuración. Revisa las cuentas sin compartir contraseñas."
        )


if __name__ == "__main__":
    main()
