from app.core.security import create_access_token, hash_password, verify_password
from app.dtos.auth import UserLogin, UserRegister
from app.exceptions.user_exceptions import (
    EmailAlreadyExistsException,
    UsernameAlreadyExistsException,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def register_user(self, data: UserRegister):
        if self.repository.get_by_email(data.email):
            raise EmailAlreadyExistsException()

        if self.repository.get_by_username(data.username):
            raise UsernameAlreadyExistsException()

        user = User(
            username=data.username,
            email=data.email,
            password=hash_password(data.password),
        )

        self.repository.create(user)

        return {
            "access_token": create_access_token(user.id),
            "refresh_token": "refreshToken",
        }

    def authenticate_user(self, data: UserLogin):
        user = self.repository.get_by_email(data.email)
        if user is None:
            return None

        authenticated = verify_password(data.password, user.password)

        if not authenticated:
            return None

        return {
            "access_token": create_access_token(user.id),
            "refresh_token": "refreshToken",
        }
