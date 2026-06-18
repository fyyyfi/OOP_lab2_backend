"""Common model building blocks shared through inheritance."""
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer


class TimestampMixin:
    """Mixin that adds auto-managed ``created_at`` / ``updated_at`` columns.

    Every domain model inherits from this mixin, an example of reusing
    behaviour through inheritance instead of duplicating columns.
    """

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
