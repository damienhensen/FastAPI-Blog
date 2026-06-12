from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends

from app.dependencies.auth import get_auth_service
from app.dtos.auth import AuthResponse, UserLogin
from app.services.auth_service import AuthService

ServiceDep = Annotated[
    AuthService,
    Depends(get_auth_service),
]

router = APIRouter(tags=["auth"])


@router.post("/login", response_model=AuthResponse, status_code=status.HTTP_200_OK)
async def authenticate_user(data: UserLogin, service: ServiceDep):
    authenticated = service.authenticate_user(data)

    if not authenticated:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or password incorrect",
        )

    return {
        "access_token": "access",
        "refresh_token": "refresh",
    }
