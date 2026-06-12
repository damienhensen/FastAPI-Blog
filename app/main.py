from fastapi import FastAPI, APIRouter

from app.routers import users, auth, blog

app = FastAPI(title="FastAPI Blog")
router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "healthy"}


app.include_router(users.router)
app.include_router(auth.router)
app.include_router(blog.router)
app.include_router(router)
