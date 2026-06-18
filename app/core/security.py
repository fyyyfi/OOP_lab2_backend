"""Password hashing and JWT helpers."""
from datetime import datetime, timedelta, timezone

import bcrypt
from jose import JWTError, jwt

from app.core.config import get_settings
from app.core.logging_config import get_logger

logger = get_logger(__name__)
settings = get_settings()

# bcrypt operates on at most 72 bytes; longer input is truncated as is standard.
_MAX_PASSWORD_BYTES = 72


def _to_bytes(password: str) -> bytes:
    return password.encode("utf-8")[:_MAX_PASSWORD_BYTES]


def hash_password(plain_password: str) -> str:
    """Return a bcrypt hash for the given password."""
    hashed = bcrypt.hashpw(_to_bytes(plain_password), bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check a plain password against a stored hash."""
    return bcrypt.checkpw(_to_bytes(plain_password), hashed_password.encode("utf-8"))


def create_access_token(subject: str, role: str) -> str:
    """Create a signed JWT for an authenticated user."""
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    payload = {"sub": subject, "role": role, "exp": expire}
    token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    logger.debug("Issued access token for subject=%s role=%s", subject, role)
    return token


def decode_access_token(token: str) -> dict:
    """Decode and validate a JWT, raising JWTError if invalid."""
    try:
        return jwt.decode(
            token, settings.jwt_secret, algorithms=[settings.jwt_algorithm]
        )
    except JWTError as exc:
        logger.warning("Rejected invalid token: %s", exc)
        raise
