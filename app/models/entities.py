from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base, utcnow


class UsuarioRol(Base):
    __tablename__ = "usuarios_roles"
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), primary_key=True)
    rol_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), primary_key=True)


class Rol(Base):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(30), unique=True)


class Usuario(Base):
    __tablename__ = "usuarios"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120))
    documento: Mapped[str] = mapped_column(String(30))
    correo: Mapped[str] = mapped_column(String(254), unique=True)
    hash_contrasena: Mapped[str] = mapped_column(Text)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    auth_version: Mapped[int] = mapped_column(default=1)
    creado_en: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    roles: Mapped[list[Rol]] = relationship(secondary="usuarios_roles", lazy="selectin")


class Servicio(Base):
    __tablename__ = "servicios"
    __table_args__ = (
        CheckConstraint("prioridad IN ('baja','normal','alta')"),
        CheckConstraint("plazo_horas IS NULL OR plazo_horas BETWEEN 1 AND 8760"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), unique=True)
    activo: Mapped[bool] = mapped_column(default=True)
    prioridad: Mapped[str] = mapped_column(String(10), default="normal")
    plazo_horas: Mapped[int | None] = mapped_column(Integer)


class Solicitud(Base):
    __tablename__ = "solicitudes"
    __table_args__ = (
        CheckConstraint(
            "estado IN ('registrada','en_revision','pendiente_informacion','aceptada','asignada','en_atencion','finalizada','rechazada','cancelada','cerrada_duplicidad')"
        ),
        Index("ix_solicitud_filtros", "estado", "creada_en", "id"),
    )
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    radicado: Mapped[str | None] = mapped_column(String(40), unique=True)
    solicitante_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), index=True)
    servicio_id: Mapped[int] = mapped_column(ForeignKey("servicios.id"), index=True)
    responsable_id: Mapped[int | None] = mapped_column(ForeignKey("usuarios.id"), index=True)
    nombre: Mapped[str] = mapped_column(String(120))
    documento: Mapped[str] = mapped_column(String(30))
    correo: Mapped[str] = mapped_column(String(254))
    asunto: Mapped[str] = mapped_column(String(150))
    descripcion: Mapped[str] = mapped_column(Text)
    estado: Mapped[str] = mapped_column(String(30), default="registrada")
    prioridad: Mapped[str] = mapped_column(String(10), default="normal", index=True)
    plazo_horas: Mapped[int | None] = mapped_column(Integer)
    respuesta_final: Mapped[str | None] = mapped_column(Text)
    resultado_final: Mapped[str | None] = mapped_column(Text)
    creada_en: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    actualizada_en: Mapped[datetime] = mapped_column(DateTime, default=utcnow, onupdate=utcnow)
    revision_iniciada_en: Mapped[datetime | None] = mapped_column(DateTime)
    atencion_iniciada_en: Mapped[datetime | None] = mapped_column(DateTime)
    finalizada_en: Mapped[datetime | None] = mapped_column(DateTime)
    original_id: Mapped[int | None] = mapped_column(ForeignKey("solicitudes.id"))
    version: Mapped[int] = mapped_column(default=1)
    __mapper_args__ = {"version_id_col": version}


class Intervencion(Base):
    __tablename__ = "intervenciones"
    id: Mapped[int] = mapped_column(primary_key=True)
    solicitud_id: Mapped[int] = mapped_column(ForeignKey("solicitudes.id"), index=True)
    autor_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    tipo: Mapped[str] = mapped_column(String(50))
    detalle: Mapped[str] = mapped_column(Text)
    interna: Mapped[bool] = mapped_column(default=False)
    estado_anterior: Mapped[str | None] = mapped_column(String(30))
    estado_nuevo: Mapped[str | None] = mapped_column(String(30))
    datos_cambio: Mapped[str | None] = mapped_column(Text)
    rectifica_id: Mapped[int | None] = mapped_column(ForeignKey("intervenciones.id"))
    creada_en: Mapped[datetime] = mapped_column(DateTime, default=utcnow)


class Ciclo(Base):
    __tablename__ = "ciclos_atencion"
    __table_args__ = (
        UniqueConstraint("solicitud_id", "numero"),
        CheckConstraint("plazo_horas IS NULL OR plazo_horas BETWEEN 1 AND 8760"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    solicitud_id: Mapped[int] = mapped_column(ForeignKey("solicitudes.id"), index=True)
    numero: Mapped[int] = mapped_column(default=1)
    inicio: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    fin: Mapped[datetime | None] = mapped_column(DateTime)
    plazo_horas: Mapped[int | None] = mapped_column(Integer)
    respuesta: Mapped[str | None] = mapped_column(Text)
    resultado: Mapped[str | None] = mapped_column(Text)
    resuelto: Mapped[bool] = mapped_column(default=False)


class Requerimiento(Base):
    __tablename__ = "requerimientos_informacion"
    id: Mapped[int] = mapped_column(primary_key=True)
    solicitud_id: Mapped[int] = mapped_column(ForeignKey("solicitudes.id"), index=True)
    solicitado_por_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    pregunta: Mapped[str] = mapped_column(Text)
    etapa_retorno: Mapped[str] = mapped_column(String(30))
    respuesta: Mapped[str | None] = mapped_column(Text)
    respondido_por_id: Mapped[int | None] = mapped_column(ForeignKey("usuarios.id"))
    creado_en: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    respondido_en: Mapped[datetime | None] = mapped_column(DateTime)
    cerrado_en: Mapped[datetime | None] = mapped_column(DateTime)
    motivo_cierre: Mapped[str | None] = mapped_column(Text)


Index(
    "uq_requerimiento_abierto",
    Requerimiento.solicitud_id,
    unique=True,
    sqlite_where=Requerimiento.cerrado_en.is_(None),
)


class Reapertura(Base):
    __tablename__ = "peticiones_reapertura"
    id: Mapped[int] = mapped_column(primary_key=True)
    solicitud_id: Mapped[int] = mapped_column(ForeignKey("solicitudes.id"), index=True)
    solicitante_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    motivo: Mapped[str] = mapped_column(Text)
    estado: Mapped[str] = mapped_column(String(20), default="pendiente")
    resuelto_por_id: Mapped[int | None] = mapped_column(ForeignKey("usuarios.id"))
    motivo_decision: Mapped[str | None] = mapped_column(Text)
    creado_en: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    resuelto_en: Mapped[datetime | None] = mapped_column(DateTime)


Index(
    "uq_reapertura_pendiente",
    Reapertura.solicitud_id,
    unique=True,
    sqlite_where=Reapertura.estado == "pendiente",
)


class Notificacion(Base):
    __tablename__ = "notificaciones"
    id: Mapped[int] = mapped_column(primary_key=True)
    destinatario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), index=True)
    solicitud_id: Mapped[int] = mapped_column(ForeignKey("solicitudes.id"))
    mensaje: Mapped[str] = mapped_column(Text)
    creada_en: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    leida_en: Mapped[datetime | None] = mapped_column(DateTime)
