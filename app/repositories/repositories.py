"""Concrete repositories.

Each class inherits :class:`BaseRepository` and may override or extend its
behaviour — a practical example of inheritance and polymorphism.
"""
from sqlalchemy.orm import Session

from app.models import Brigade, Request, Specialist, User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session) -> None:
        super().__init__(User, db)

    def get_by_username(self, username: str) -> User | None:
        return self._db.query(User).filter(User.username == username).first()


class SpecialistRepository(BaseRepository[Specialist]):
    def __init__(self, db: Session) -> None:
        super().__init__(Specialist, db)

    def list_available_by_specialty(self, specialty: str) -> list[Specialist]:
        return (
            self._db.query(Specialist)
            .filter(
                Specialist.specialty == specialty,
                Specialist.is_available.is_(True),
            )
            .all()
        )

    def get_many(self, ids: list[int]) -> list[Specialist]:
        if not ids:
            return []
        return self._db.query(Specialist).filter(Specialist.id.in_(ids)).all()


class RequestRepository(BaseRepository[Request]):
    def __init__(self, db: Session) -> None:
        super().__init__(Request, db)


class BrigadeRepository(BaseRepository[Brigade]):
    def __init__(self, db: Session) -> None:
        super().__init__(Brigade, db)

    def list(self) -> list[Brigade]:
        # Polymorphic override: brigades are ordered by their schedule.
        return self._db.query(Brigade).order_by(Brigade.scheduled_at).all()
