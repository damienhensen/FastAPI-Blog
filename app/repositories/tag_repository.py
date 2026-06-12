from sqlalchemy.orm import Session

from app.models.tag import Tag


class TagRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_name(self, name: str):
        return self.db.query(Tag).filter(Tag.name == name).first()

    def create(self, tag: Tag):
        self.db.add(tag)
        self.db.commit()
        self.db.refresh(tag)
        return tag
