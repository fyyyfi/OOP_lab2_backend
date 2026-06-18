"""Authentication business logic."""
from sqlalchemy.orm import Session

from app.core.logging_config import get_logger
from app.core.security import create_access_token, hash_password, verify_password
from app.models import User
from app.repositories.repositories import UserRepository
from app.services.exceptions import AuthError, ValidationError

logger = get_logger(__name__)


class AuthService:
    """Handles registration and login."""

    def __init__(self, db: Session) -> None:
        self._users = UserRepository(db)

    def register(self, username: str, full_name: str, password: str, role: str) -> User:
        if self._users.get_by_username(username):
            raise ValidationError(f"Username '{username}' is already taken")
        user = self._users.create(
            username=username,
            full_name=full_name,
            hashed_password=hash_password(password),
            role=role,
        )
        logger.info("Registered user '%s' with role '%s'", username, role)
        return user

    def authenticate(self, username: str, password: str) -> tuple[str, User]:
        user = self._users.get_by_username(username)
        if not user or not verify_password(password, user.hashed_password):
            logger.warning("Failed login attempt for username '%s'", username)
            raise AuthError("Invalid username or password")
        token = create_access_token(subject=user.username, role=user.role)
        logger.info("User '%s' logged in", username)
        return token, user
