from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends

from app.dependencies.auth import get_auth_service, get_current_user
from app.dtos.auth import AuthResponse, UserLogin, UserRegister
from app.dtos.user import UserResponse
from app.exceptions.user_exceptions import (
    EmailAlreadyExistsException,
    UsernameAlreadyExistsException,
)
from app.models.user import User
from app.services.auth_service import AuthService

ServiceDep = Annotated[
    AuthService,
    Depends(get_auth_service),
]

CurrentUserDep = Annotated[
    User,
    Depends(get_current_user),
]

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def me(current_user: CurrentUserDep):
    return current_user


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_200_OK)
async def register_user(new_user: UserRegister, service: ServiceDep):
    try:
        return service.register_user(new_user)
    except EmailAlreadyExistsException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already in use",
        )
    except UsernameAlreadyExistsException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already in use",
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create user",
        )


@router.post("/login", response_model=AuthResponse, status_code=status.HTTP_200_OK)
async def authenticate_user(data: UserLogin, service: ServiceDep):
    authenticated = service.authenticate_user(data)

    if not authenticated:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or password incorrect",
        )

    return authenticated
