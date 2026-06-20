from sqlalchemy import Boolean, Column, String

from app.core.database import Base
from app.models.base import TimestampMixin


class Specialist(TimestampMixin, Base):
    """A worker with a particular specialty (electrical, plumbing, ...)."""

    __tablename__ = "specialists"

    full_name = Column(String(128), nullable=False)
    # Matches Request.work_type, e.g. "electrical", "plumbing", "general".
    specialty = Column(String(32), nullable=False, index=True)
    is_available = Column(Boolean, nullable=False, default=True)
