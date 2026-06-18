"""Service-request endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.controllers.dependencies import get_current_user, require_dispatcher
from app.core.database import get_db
from app.schemas.request import RequestCreate, RequestResponse, RequestUpdate
from app.services.exceptions import ServiceError
from app.services.request_service import RequestService

router = APIRouter(prefix="/api/requests", tags=["requests"])


@router.get("", response_model=list[RequestResponse])
def list_requests(
    db: Session = Depends(get_db), _: dict = Depends(get_current_user)
) -> list[RequestResponse]:
    return [RequestResponse.model_validate(r) for r in RequestService(db).list()]


@router.get("/{request_id}", response_model=RequestResponse)
def get_request(
    request_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_user),
) -> RequestResponse:
    try:
        return RequestResponse.model_validate(RequestService(db).get(request_id))
    except ServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc))


@router.post("", response_model=RequestResponse, status_code=201)
def create_request(
    payload: RequestCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_user),
) -> RequestResponse:
    return RequestResponse.model_validate(RequestService(db).create(payload))


@router.put("/{request_id}", response_model=RequestResponse)
def update_request(
    request_id: int,
    payload: RequestUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(require_dispatcher),
) -> RequestResponse:
    try:
        return RequestResponse.model_validate(
            RequestService(db).update(request_id, payload)
        )
    except ServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc))


@router.delete("/{request_id}", status_code=204)
def delete_request(
    request_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(require_dispatcher),
) -> None:
    try:
        RequestService(db).delete(request_id)
    except ServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc))
