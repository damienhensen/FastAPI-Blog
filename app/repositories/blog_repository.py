from sqlalchemy.orm import Session, joinedload, selectinload

from app.models.post import Post


class BlogRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return (
            self.db.query(Post)
            .options(
                joinedload(Post.author),
                joinedload(Post.category),
                selectinload(Post.tags),
            )
            .all()
        )
