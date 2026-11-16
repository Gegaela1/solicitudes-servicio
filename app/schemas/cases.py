from app.schemas.common import Reason
from datetime import date
from typing import Literal
from pydantic import Field, model_validator
from app.schemas.common import Identity, Input, Text


class CaseCreate(Identity):
    servicio_id: int = Field(gt=0)
    asunto: Text = Field(min_length=5, max_length=150)
    descripcion: Text = Field(min_length=20, max_length=5000)


class Action(Input):
    version: int = Field(ge=1)


State = Literal[
    "registrada",
    "en_revision",
    "pendiente_informacion",
    "aceptada",
    "asignada",
    "en_atencion",
    "finalizada",
    "rechazada",
    "cancelada",
    "cerrada_duplicidad",
]
Priority = Literal["baja", "normal", "alta"]


class Filters(Input):
    page: int = Field(default=1, ge=1)
    size: int = Field(default=20, ge=1, le=100)
    estado: State | None = None
    responsable_id: int | None = Field(default=None, gt=0)
    servicio_id: int | None = Field(default=None, gt=0)
    prioridad: Priority | None = None
    desde: date | None = None
    hasta: date | None = None
    radicado: str | None = Field(default=None, max_length=40)

    @model_validator(mode="after")
    def dates(self):
        if self.desde and self.hasta and self.desde > self.hasta:
            raise ValueError("Rango de fechas inválido")
        return self


class Note(Action):
    detalle: Text = Field(min_length=1, max_length=5000)
    interna: bool = True
    rectifica_id: int | None = Field(default=None, gt=0)


class Motive(Action):
    motivo: Reason


class Assign(Motive):
    responsable_id: int = Field(gt=0)


class Finalize(Action):
    respuesta: Text = Field(min_length=10, max_length=5000)
    resultado: Text = Field(min_length=5, max_length=2000)


class Question(Action):
    pregunta: Reason


class Answer(Action):
    respuesta: Text = Field(min_length=1, max_length=5000)


class Correction(CaseCreate):
    version: int = Field(ge=1)
    motivo: Reason | None = None


class ReopenDecision(Motive):
    aprobar: bool


class Duplicate(Motive):
    original_id: int = Field(gt=0)
