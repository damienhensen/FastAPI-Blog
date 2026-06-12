from datetime import datetime

from pydantic import BaseModel


class BlogListResponse(BaseModel):
    author: str
    category: str
    tags: list[str]
    slug: str
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
