"""Specialist endpoints (protected for write operations)."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.controllers.dependencies import get_current_user, require_dispatcher
from app.core.database import get_db
from app.schemas.specialist import (
    SpecialistCreate,
    SpecialistResponse,
    SpecialistUpdate,
)
from app.services.exceptions import ServiceError
from app.services.specialist_service import SpecialistService

router = APIRouter(prefix="/api/specialists", tags=["specialists"])


@router.get("", response_model=list[SpecialistResponse])
def list_specialists(
    db: Session = Depends(get_db), _: dict = Depends(get_current_user)
) -> list[SpecialistResponse]:
    return [SpecialistResponse.model_validate(s) for s in SpecialistService(db).list()]


@router.post("", response_model=SpecialistResponse, status_code=201)
def create_specialist(
    payload: SpecialistCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_dispatcher),
) -> SpecialistResponse:
    return SpecialistResponse.model_validate(SpecialistService(db).create(payload))


@router.put("/{specialist_id}", response_model=SpecialistResponse)
def update_specialist(
    specialist_id: int,
    payload: SpecialistUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_dispatcher),
) -> SpecialistResponse:
    try:
        return SpecialistResponse.model_validate(
            SpecialistService(db).update(specialist_id, payload)
        )
    except ServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc))


@router.delete("/{specialist_id}", status_code=204)
def delete_specialist(
    specialist_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_dispatcher),
) -> None:
    try:
        SpecialistService(db).delete(specialist_id)
    except ServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc))
