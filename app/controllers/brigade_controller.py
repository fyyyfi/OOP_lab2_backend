"""Brigade / work-plan endpoints (dispatcher only)."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.controllers.dependencies import get_current_user, require_dispatcher
from app.core.database import get_db
from app.schemas.brigade import BrigadeCreate, BrigadeResponse
from app.services.brigade_service import BrigadeService
from app.services.exceptions import ServiceError

router = APIRouter(prefix="/api/brigades", tags=["brigades"])


@router.get("", response_model=list[BrigadeResponse])
def list_brigades(
    db: Session = Depends(get_db), _: dict = Depends(get_current_user)
) -> list[BrigadeResponse]:
    return [BrigadeResponse.model_validate(b) for b in BrigadeService(db).list()]


@router.post("", response_model=BrigadeResponse, status_code=201)
def create_brigade(
    payload: BrigadeCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_dispatcher),
) -> BrigadeResponse:
    try:
        return BrigadeResponse.model_validate(BrigadeService(db).create(payload))
    except ServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc))


@router.delete("/{brigade_id}", status_code=204)
def delete_brigade(
    brigade_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_dispatcher),
) -> None:
    try:
        BrigadeService(db).delete(brigade_id)
    except ServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc))
