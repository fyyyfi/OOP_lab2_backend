from sqlalchemy import Column, String

from app.core.database import Base
from app.models.base import TimestampMixin


class User(TimestampMixin, Base):
    """An application user (dispatcher or tenant)."""

    __tablename__ = "users"

    username = Column(String(64), unique=True, index=True, nullable=False)
    full_name = Column(String(128), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    # "dispatcher" users may manage brigades and the work plan.
    role = Column(String(32), nullable=False, default="tenant")
