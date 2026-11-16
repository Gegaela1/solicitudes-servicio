from pathlib import Path

from pydantic import Field, SecretStr, ValidationError, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ROOT / ".env", extra="ignore")
    database_url: str = "sqlite:///./solicitudes.db"
    secret_key: SecretStr
    access_token_expire_minutes: int = Field(default=30, ge=1, le=1440)
    app_env: str = "development"

    @field_validator("database_url")
    @classmethod
    def sqlite_url(cls, value):
        if not value.startswith("sqlite:///"):
            raise ValueError("Esta versión requiere una base SQLite local")
        return value

    @field_validator("secret_key")
    @classmethod
    def strong_key(cls, value):
        if len(value.get_secret_value()) < 32:
            raise ValueError("La clave debe tener al menos 32 caracteres")
        return value


def load_settings():
    try:
        return Settings()
    except ValidationError:
        raise RuntimeError(
            "Configuración inválida. Revisa .env sin compartir sus secretos."
        ) from None
