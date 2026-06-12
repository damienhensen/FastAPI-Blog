from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends

from app.dependencies.auth import get_current_user
from app.dependencies.users import get_user_service
from app.dtos.user import UserResponse, UserUpdate
from app.models.user import User
from app.services.user_service import UserService

ServiceDep = Annotated[
    UserService,
    Depends(get_user_service),
]

CurrentUserDep = Annotated[
    User,
    Depends(get_current_user),
]

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserResponse])
async def read_users(service: ServiceDep):
    return service.get_all_users()


@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def read_user(user_id: int, service: ServiceDep):
    user = service.get_user(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user


@router.patch("/", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_user(
    data: UserUpdate, current_user: CurrentUserDep, service: ServiceDep
):
    user = service.update_user(current_user.id, data)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(current_user: CurrentUserDep, service: ServiceDep):
    deleted = service.delete_user(current_user.id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return
