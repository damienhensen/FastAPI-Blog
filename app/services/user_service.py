from app.dtos.user import UserCreate, UserUpdate
from app.models.user import User
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_all_users(self):
        return self.repository.get_all()

    def get_user(self, user_id: int):
        return self.repository.get_by_id(user_id)

    def create_user(self, data: UserCreate):
        user = User(
            username=data.username,
            email=data.email,
            password=data.password,  # TODO: HASH PASSWORD
        )

        return self.repository.create(user)

    def update_user(self, user_id: int, data: UserUpdate):
        user = self.repository.get_by_id(user_id)

        if user is None:
            return None

        if data.username is not None:
            user.username = data.username

        if data.email is not None:
            user.email = data.email

        return self.repository.update(user)

    def delete_user(self, user_id: int):
        user = self.repository.get_by_id(user_id)

        if user is None:
            return False

        self.repository.delete(user)

        return True
