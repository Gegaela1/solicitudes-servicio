"""Genera cuentas ficticias, exclusivamente para demostración local."""

import json
import secrets
from pathlib import Path
from sqlalchemy import select
from app.db.session import SessionLocal
from app.models.entities import Usuario, Rol
from app.core.security import password_hash
from scripts.preparar import seed


def main():
    seed()
    access = []
    with SessionLocal.begin() as db:
        for label, role in [
            ("solicitante", "solicitante"),
            ("atencion", "atencion"),
            ("coordinacion", "coordinacion"),
        ]:
            email = f"demo.{label}@example.com"
            if db.scalar(select(Usuario).where(Usuario.correo == email)):
                print(f"Se conserva la cuenta demo existente: {email}")
                continue
            password = secrets.token_urlsafe(18)
            user = Usuario(
                nombre="Demo " + label,
                documento="DEMO-" + label,
                correo=email,
                hash_contrasena=password_hash.hash(password),
                roles=list(db.scalars(select(Rol).where(Rol.nombre == role))),
            )
            db.add(user)
            access.append({"rol": role, "correo": email, "contrasena": password})
    if access:
        p = Path("work/demo-acceso.json")
        p.parent.mkdir(exist_ok=True)
        # No sobrescribir credenciales de cuentas conservadas.
        previous = json.loads(p.read_text(encoding="utf-8")) if p.exists() else []
        p.write_text(json.dumps(previous + access, ensure_ascii=False, indent=2), encoding="utf-8")
        print(
            "Credenciales demo generadas en work/demo-acceso.json; archivo local excluido de Git. No compartir ni usar en producción."
        )
    else:
        print("No se crearon cuentas nuevas; no se cambiaron contraseñas.")


if __name__ == "__main__":
    main()
