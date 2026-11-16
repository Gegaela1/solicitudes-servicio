from typing import Literal
from pydantic import Field
from app.schemas.common import Input, Registration

RoleName = Literal["solicitante", "atencion", "coordinacion"]


class StaffCreate(Registration):
    roles: list[RoleName] = Field(min_length=1, max_length=3)


class StaffUpdate(Input):
    roles: list[RoleName] = Field(min_length=1, max_length=3)
    activo: bool
