from app.core.security import verify_password
from app.dtos.auth import UserLogin
from app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def authenticate_user(self, data: UserLogin):
        user = self.repository.get_by_email(data.email)
        if user is None:
            return False

        return verify_password(data.password, user.password)
