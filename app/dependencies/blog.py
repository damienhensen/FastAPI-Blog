from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.blog_repository import BlogRepository
from app.services.blog_service import BlogService


def get_blog_service(db: Session = Depends(get_db)):
    repository = BlogRepository(db)
    return BlogService(repository)
