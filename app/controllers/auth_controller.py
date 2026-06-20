from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.controllers.dependencies import get_current_user
from app.core.database import get_db
from app.schemas.auth import LoginRequest, TokenResponse, UserCreate, UserResponse
from app.services.auth_service import AuthService
from app.services.exceptions import ServiceError

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=201)
def register(payload: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    try:
        user = AuthService(db).register(
            payload.username, payload.full_name, payload.password, payload.role
        )
    except ServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc))
    return UserResponse.model_validate(user)


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    try:
        token, user = AuthService(db).authenticate(payload.username, payload.password)
    except ServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc))
    return TokenResponse(access_token=token, role=user.role, full_name=user.full_name)


@router.get("/me", response_model=dict)
def me(current_user: dict = Depends(get_current_user)) -> dict:
    """Return the claims of the authenticated user (protected endpoint)."""
    return {"username": current_user["sub"], "role": current_user["role"]}
