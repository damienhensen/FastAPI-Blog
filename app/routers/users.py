from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends

from app.dependencies.users import get_user_service
from app.dtos.user import UserResponse, UserUpdate
from app.services.user_service import UserService

ServiceDep = Annotated[
    UserService,
    Depends(get_user_service),
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


@router.patch("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_user(user_id: int, data: UserUpdate, service: ServiceDep):
    user = service.update_user(user_id, data)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, service: ServiceDep):
    deleted = service.delete_user(user_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return
