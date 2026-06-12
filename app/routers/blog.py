from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependencies.auth import get_current_user
from app.dependencies.blog import get_blog_service
from app.dtos.blog import BlogListResponse
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
