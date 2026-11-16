from pydantic import Field
from app.schemas.common import Identity, Input, Text


class CaseCreate(Identity):
    servicio_id: int = Field(gt=0)
    asunto: Text = Field(min_length=5, max_length=150)
    descripcion: Text = Field(min_length=20, max_length=5000)


class Action(Input):
    version: int = Field(ge=1)
