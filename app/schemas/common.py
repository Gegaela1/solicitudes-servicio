from typing import Annotated
import unicodedata
from pydantic import BaseModel, ConfigDict, EmailStr, Field, BeforeValidator, field_validator


def clean(value):
    if not isinstance(value, str):
        return value
    value = value.strip()
    if any(unicodedata.category(c).startswith("C") and c not in "\n\r\t" for c in value):
        raise ValueError("El texto contiene caracteres de control")
    return value


Text = Annotated[str, BeforeValidator(clean)]
Name = Annotated[Text, Field(min_length=2, max_length=120)]
Document = Annotated[Text, Field(min_length=3, max_length=30, pattern=r"^[^\s].*[^\s]$")]
Password = Annotated[str, Field(min_length=12, max_length=128)]
Reason = Annotated[Text, Field(min_length=10, max_length=2000)]


class Input(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Identity(Input):
    nombre: Name
    documento: Document
    correo: EmailStr = Field(max_length=254)

    @field_validator("correo", mode="before")
    @classmethod
    def email_normalized(cls, value):
        return value.strip().lower() if isinstance(value, str) else value

    @field_validator("nombre", "documento")
    @classmethod
    def single_line(cls, value):
        if any(c in value for c in "\n\r\t"):
            raise ValueError("No se permiten saltos de línea ni tabulaciones")
        return value


class Login(Input):
    correo: EmailStr
    contrasena: str = Field(min_length=1, max_length=128)

    @field_validator("correo", mode="before")
    @classmethod
    def normalize(cls, value):
        return value.strip().lower() if isinstance(value, str) else value


class PasswordChange(Input):
    actual: str = Field(min_length=1, max_length=128)
    nueva: Password


class Registration(Identity):
    contrasena: Password
