from app.models.category import Category
from app.repositories.category_repository import CategoryRepository


class CategoryService:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def create(self, name: str):
        category = Category(name=name)
        return self.repository.create(category)

    def get_by_name(self, name: str):
        return self.repository.get_by_name(name)
