from typing import Annotated

from fastapi import APIRouter, HTTPException, Response, status, Depends

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
async def register_user(
    new_user: UserRegister, response: Response, service: ServiceDep
):
    try:
        tokens = service.register_user(new_user)

        response.set_cookie(
            key="refresh_token",
            value=tokens["refresh_token"],
            httponly=True,
            secure=False,  # HTTPS
            samesite="lax",
            max_age=60 * 60 * 24 * 30,
            path="/auth",
        )

        return {"access_token": tokens["access_token"], "token_type": "bearer"}

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
async def authenticate_user(data: UserLogin, response: Response, service: ServiceDep):
    tokens = service.authenticate_user(data)

    if not tokens:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or password incorrect",
        )

    response.set_cookie(
        key="refresh_token",
        value=tokens["refresh_token"],
        httponly=True,
        secure=False,  # HTTPS
        samesite="lax",
        max_age=60 * 60 * 24 * 30,
        path="/auth",
    )

    return {"access_token": tokens["access_token"], "token_type": "bearer"}


from fastapi import Cookie


@router.post("/refresh", response_model=AuthResponse)
async def refresh(
    service: ServiceDep,
    response: Response,
    refresh_token: str | None = Cookie(default=None),
):
    if refresh_token is None:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    tokens = service.refresh_token(refresh_token)

    if tokens is None:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    response.set_cookie(
        key="refresh_token",
        value=tokens["refresh_token"],
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60 * 60 * 24 * 30,
        path="/auth",
    )

    return {
        "access_token": tokens["access_token"],
        "token_type": "bearer",
    }


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    current_user: CurrentUserDep,
    service: ServiceDep,
    response: Response,
    refresh_token: str | None = Cookie(default=None),
):
    if refresh_token:
        service.logout(current_user.id, refresh_token)

    response.delete_cookie(
        key="refresh_token",
        path="/auth",
    )

    return


@router.post("/logout-all", status_code=status.HTTP_204_NO_CONTENT)
async def logout_all(current_user: CurrentUserDep, service: ServiceDep, response: Response):
    service.logout_all(current_user.id)

    response.delete_cookie(
        key="refresh_token",
        path="/auth",
    )

    return
