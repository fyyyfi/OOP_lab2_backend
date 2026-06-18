"""Brigade business logic — assembling teams and filling the work plan."""
from sqlalchemy.orm import Session

from app.core.logging_config import get_logger
from app.models import Brigade
from app.repositories.repositories import (
    BrigadeRepository,
    RequestRepository,
    SpecialistRepository,
)
from app.schemas.brigade import BrigadeCreate
from app.services.domain import SpecialistWorker
from app.services.exceptions import NotFoundError, ValidationError

logger = get_logger(__name__)


class BrigadeService:
    """Creates brigades and registers them in the work plan."""

    def __init__(self, db: Session) -> None:
        self._brigades = BrigadeRepository(db)
        self._specialists = SpecialistRepository(db)
        self._requests = RequestRepository(db)

    def list(self) -> list[Brigade]:
        return self._brigades.list()

    def get(self, brigade_id: int) -> Brigade:
        brigade = self._brigades.get(brigade_id)
        if not brigade:
            raise NotFoundError(f"Brigade {brigade_id} not found")
        return brigade

    def create(self, data: BrigadeCreate) -> Brigade:
        request = self._requests.get(data.request_id)
        if not request:
            raise NotFoundError(f"Request {data.request_id} not found")

        specialists = self._specialists.get_many(data.specialist_ids)
        if not specialists:
            raise ValidationError("A brigade must contain at least one specialist")

        # Use the polymorphic domain model to verify the team can do the work.
        unfit = [
            s.full_name
            for s in specialists
            if not SpecialistWorker(s.full_name, s.specialty).can_handle(request.work_type)
        ]
        if unfit:
            raise ValidationError(
                f"Specialists cannot handle '{request.work_type}': {', '.join(unfit)}"
            )

        brigade = Brigade(
            name=data.name,
            request_id=data.request_id,
            scheduled_at=data.scheduled_at,
            status="planned",
        )
        brigade.specialists = specialists
        self._brigades._db.add(brigade)
        # Registering the brigade also moves the request to "assigned".
        request.status = "assigned"
        self._brigades._db.commit()
        self._brigades._db.refresh(brigade)
        logger.info(
            "Registered brigade '%s' with %d specialist(s) for request %s",
            brigade.name,
            len(specialists),
            data.request_id,
        )
        return brigade

    def delete(self, brigade_id: int) -> None:
        brigade = self.get(brigade_id)
        self._brigades.delete(brigade)
        logger.info("Deleted brigade %s", brigade_id)
