from app.models.tag import Tag
from app.repositories.tag_repository import TagRepository


class TagService:
    def __init__(self, repository: TagRepository):
        self.repository = repository

    def create(self, name: str):
        tag = Tag(name=name)
        return self.repository.create(tag)

    def get_by_name(self, name: str):
        return self.repository.get_by_name(name)
