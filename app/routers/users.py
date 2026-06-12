from fastapi import APIRouter, HTTPException, status
from app.models.user import User

router = APIRouter(prefix="/users", tags=["users"])

users = [
    User(username="Damien"),
    User(username="Pim"),
]


@router.get("/")
async def read_users():
    return users


@router.get("/me")
async def read_user_me():
    return users[0]


@router.get("/{username}", status_code=status.HTTP_200_OK)
async def read_user(username: str):
    for user in users:
        if user.username == username:
            return user

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(newUser: User):
    for user in users:
        if user.username == newUser.username:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="User already exists"
            )

    users.append(newUser)
    return {"detail": "User created"}


@router.put("/{username}", status_code=status.HTTP_200_OK)
async def update_user(username: str, newUser: User):
    for user in users:
        if user.username == username:
            user.username = newUser.username
            return {"detail": "User updated"}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.delete("/{username}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(username: str):
    for idx, user in enumerate(users):
        if user.username == username:
            users.pop(idx)
            return

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
