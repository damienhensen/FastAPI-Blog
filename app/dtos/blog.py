from datetime import datetime

from pydantic import BaseModel


class BlogListResponse(BaseModel):
    title: str
    slug: str
    author: str
    category: str
    tags: list[str]
    created_at: datetime
    updated_at: datetime


class BlogCreate(BaseModel):
    title: str
    content: str
    category: str
    tags: list[str]
    slug: str | None = None
