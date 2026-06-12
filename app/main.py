from fastapi import FastAPI, APIRouter

from .routers import users

app = FastAPI(title="FastAPI Blog")
router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "healthy"}


app.include_router(users.router)
app.include_router(router)