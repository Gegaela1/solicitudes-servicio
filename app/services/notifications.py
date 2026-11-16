from sqlalchemy import select
from app.models.entities import Usuario, Rol, Notificacion


def notify(db, case, kind, internal):
    recipients = set()
    if not internal:
        recipients.add(case.solicitante_id)
    if case.responsable_id:
        recipients.add(case.responsable_id)
    staff_roles = ["coordinacion", "atencion"] if kind == "registro" else ["coordinacion"]
    recipients.update(
        db.scalars(
            select(Usuario.id).where(
                Usuario.activo.is_(True), Usuario.roles.any(Rol.nombre.in_(staff_roles))
            )
        )
    )
    for uid in recipients:
        db.add(
            Notificacion(
                destinatario_id=uid,
                solicitud_id=case.id,
                mensaje=f"{case.radicado}: {kind.replace('_', ' ')}",
            )
        )
