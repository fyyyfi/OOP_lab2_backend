"""Specialist business logic."""
from sqlalchemy.orm import Session

from app.core.logging_config import get_logger
from app.models import Specialist
from app.repositories.repositories import SpecialistRepository
from app.schemas.specialist import SpecialistCreate, SpecialistUpdate
from app.services.exceptions import NotFoundError

logger = get_logger(__name__)


class SpecialistService:
    def __init__(self, db: Session) -> None:
        self._repo = SpecialistRepository(db)

    def list(self) -> list[Specialist]:
        return self._repo.list()

    def get(self, specialist_id: int) -> Specialist:
        specialist = self._repo.get(specialist_id)
        if not specialist:
            raise NotFoundError(f"Specialist {specialist_id} not found")
        return specialist

    def create(self, data: SpecialistCreate) -> Specialist:
        specialist = self._repo.create(**data.model_dump())
        logger.info("Created specialist '%s' (%s)", specialist.full_name, specialist.specialty)
        return specialist

    def update(self, specialist_id: int, data: SpecialistUpdate) -> Specialist:
        specialist = self.get(specialist_id)
        updated = self._repo.update(specialist, **data.model_dump(exclude_unset=True))
        logger.info("Updated specialist %s", specialist_id)
        return updated

    def delete(self, specialist_id: int) -> None:
        specialist = self.get(specialist_id)
        self._repo.delete(specialist)
        logger.info("Deleted specialist %s", specialist_id)
