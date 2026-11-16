import secrets
from pathlib import Path

p = Path(".env")
if p.exists():
    print("Se conserva .env existente.")
else:
    p.write_text(
        "DATABASE_URL=sqlite:///./solicitudes.db\nSECRET_KEY="
        + secrets.token_urlsafe(48)
        + "\nACCESS_TOKEN_EXPIRE_MINUTES=30\nAPP_ENV=development\n",
        encoding="utf-8",
    )
    print(".env creado con clave aleatoria; no compartir.")
