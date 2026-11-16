from datetime import datetime, timedelta, timezone
import jwt
from pwdlib import PasswordHash
from app.core.config import load_settings

settings = load_settings()
password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash("valor-aleatorio-no-cuenta-12345")
ALGORITHM = "HS256"


def token_for(user):
    now = datetime.now(timezone.utc)
    return jwt.encode(
        {
            "sub": str(user.id),
            "ver": user.auth_version,
            "iat": now,
            "exp": now + timedelta(minutes=settings.access_token_expire_minutes),
        },
        settings.secret_key.get_secret_value(),
        algorithm=ALGORITHM,
    )


def verify_password(plain, hashed):
    return password_hash.verify(plain, hashed)
