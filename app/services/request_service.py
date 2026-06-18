"""Service-request business logic."""
from sqlalchemy.orm import Session

from app.core.logging_config import get_logger
from app.models import Request
from app.repositories.repositories import RequestRepository
from app.schemas.request import RequestCreate, RequestUpdate
from app.services.exceptions import NotFoundError

logger = get_logger(__name__)


class RequestService:
    def __init__(self, db: Session) -> None:
        self._repo = RequestRepository(db)

    def list(self) -> list[Request]:
        return self._repo.list()

    def get(self, request_id: int) -> Request:
        request = self._repo.get(request_id)
        if not request:
            raise NotFoundError(f"Request {request_id} not found")
        return request

    def create(self, data: RequestCreate) -> Request:
        request = self._repo.create(**data.model_dump(), status="new")
        logger.info("Created request from '%s' (%s)", request.tenant_name, request.work_type)
        return request

    def update(self, request_id: int, data: RequestUpdate) -> Request:
        request = self.get(request_id)
        updated = self._repo.update(request, **data.model_dump(exclude_unset=True))
        logger.info("Updated request %s", request_id)
        return updated

    def delete(self, request_id: int) -> None:
        request = self.get(request_id)
        self._repo.delete(request)
        logger.info("Deleted request %s", request_id)
