from app.dtos.user import UserUpdate
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_all_users(self):
        return self.repository.get_all()

    def get_user(self, user_id: int):
        return self.repository.get_by_id(user_id)

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
