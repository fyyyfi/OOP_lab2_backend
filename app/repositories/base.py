"""Generic repository implementing common CRUD operations.

This base class is reused by every concrete repository through inheritance,
giving consistent data-access behaviour with no duplicated SQL code.
"""
from typing import Generic, TypeVar

from sqlalchemy.orm import Session

from app.core.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """CRUD operations for a single ORM model."""

    def __init__(self, model: type[ModelType], db: Session) -> None:
        # ``_model`` and ``_db`` are kept protected (encapsulation): callers
        # interact through methods, not by touching the session directly.
        self._model = model
        self._db = db

    def list(self) -> list[ModelType]:
        return self._db.query(self._model).order_by(self._model.id).all()

    def get(self, entity_id: int) -> ModelType | None:
        return self._db.get(self._model, entity_id)

    def create(self, **fields) -> ModelType:
        entity = self._model(**fields)
        self._db.add(entity)
        self._db.commit()
        self._db.refresh(entity)
        return entity

    def update(self, entity: ModelType, **fields) -> ModelType:
        for key, value in fields.items():
            if value is not None:
                setattr(entity, key, value)
        self._db.commit()
        self._db.refresh(entity)
        return entity

    def delete(self, entity: ModelType) -> None:
        self._db.delete(entity)
        self._db.commit()
