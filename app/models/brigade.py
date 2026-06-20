from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.base import TimestampMixin

# Many-to-many link between brigades and their specialists.
brigade_specialists = Table(
    "brigade_specialists",
    Base.metadata,
    Column("brigade_id", ForeignKey("brigades.id", ondelete="CASCADE"), primary_key=True),
    Column("specialist_id", ForeignKey("specialists.id", ondelete="CASCADE"), primary_key=True),
)


class Brigade(TimestampMixin, Base):
    """A team of specialists scheduled to fulfil a request.

    A brigade that has a ``scheduled_at`` value is considered registered in
    the work plan (План робіт).
    """

    __tablename__ = "brigades"

    name = Column(String(128), nullable=False)
    request_id = Column(
        Integer, ForeignKey("requests.id", ondelete="CASCADE"), nullable=False
    )
    scheduled_at = Column(DateTime, nullable=True)
    status = Column(String(32), nullable=False, default="planned")

    request = relationship("Request")
    specialists = relationship("Specialist", secondary=brigade_specialists)
