from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/users", tags=["users"])

users = [
    {
        "username": "Damien",
    },
    {"username": "Pim"},
]


@router.get("/")
async def read_users():
    return users


@router.get("/me")
async def read_user_me():
    return users[0]


@router.get("/{username}")
async def read_user(username: str):
    for user in users:
        if user["username"] == username:
            return user

    raise HTTPException(status_code=404, detail="User not found")
