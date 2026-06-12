from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.dependencies.auth import get_current_user
from app.dependencies.blog import get_blog_service
from app.dtos.blog import BlogCreate, BlogListResponse
from app.models.user import User
from app.services.blog_service import BlogService

ServiceDep = Annotated[
    BlogService,
    Depends(get_blog_service),
]

CurrentUserDep = Annotated[
    User,
    Depends(get_current_user),
]

router = APIRouter(prefix="/blog", tags=["blog"])


@router.get("/", response_model=list[BlogListResponse])
async def read_blogs(service: ServiceDep):
    return service.get_all_posts()


@router.post("/", response_model=BlogListResponse, status_code=status.HTTP_201_CREATED)
async def create_blog(
    blog: BlogCreate, current_user: CurrentUserDep, service: ServiceDep
):
    return service.create_post(current_user.id, blog)
