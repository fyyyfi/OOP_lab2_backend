"""ORM models package.

Importing every model here guarantees that Alembic's autogenerate and
``Base.metadata.create_all`` see the complete schema.
"""
from app.models.user import User
from app.models.specialist import Specialist
from app.models.request import Request
from app.models.brigade import Brigade, brigade_specialists

__all__ = ["User", "Specialist", "Request", "Brigade", "brigade_specialists"]
