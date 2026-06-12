from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.blog_repository import BlogRepository
from app.repositories.category_repository import CategoryRepository
from app.repositories.tag_repository import TagRepository
from app.services.blog_service import BlogService
from app.services.category_service import CategoryService
from app.services.tag_service import TagService


def get_blog_service(db: Session = Depends(get_db)):
    repository = BlogRepository(db)
    category_repository = CategoryRepository(db)
    category_service = CategoryService(category_repository)
    tag_repository = TagRepository(db)
    tag_service = TagService(tag_repository)
    return BlogService(repository, category_service, tag_service)
