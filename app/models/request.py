from sqlalchemy import Column, DateTime, Integer, String, Text

from app.core.database import Base
from app.models.base import TimestampMixin


class Request(TimestampMixin, Base):
    """A maintenance request describing the type and volume of work."""

    __tablename__ = "requests"

    tenant_name = Column(String(128), nullable=False)
    address = Column(String(255), nullable=False)
    # electrical / plumbing / general ...
    work_type = Column(String(32), nullable=False, index=True)
    description = Column(Text, nullable=False, default="")
    # Estimated volume of work, in person-hours.
    volume_hours = Column(Integer, nullable=False, default=1)
    desired_time = Column(DateTime, nullable=True)
    # new -> assigned -> done
    status = Column(String(32), nullable=False, default="new")
