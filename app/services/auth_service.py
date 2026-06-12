from app.core.security import create_access_token, hash_password, verify_password
from app.dtos.auth import UserLogin, UserRegister
from app.exceptions.user_exceptions import (
    EmailAlreadyExistsException,
    UsernameAlreadyExistsException,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.services.refresh_token_service import RefreshTokenService


class AuthService:
    def __init__(
        self, repository: UserRepository, refresh_token_service: RefreshTokenService
    ):
        self.repository = repository
        self.refresh_token_service = refresh_token_service

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

        refreshToken = self.refresh_token_service.create_token(user.id)

        return {
            "access_token": create_access_token(user.id),
            "refresh_token": refreshToken,
        }

    def authenticate_user(self, data: UserLogin):
        user = self.repository.get_by_email(data.email)
        if user is None:
            return None

        authenticated = verify_password(data.password, user.password)

        if not authenticated:
            return None

        refreshToken = self.refresh_token_service.create_token(user.id)

        return {
            "access_token": create_access_token(user.id),
            "refresh_token": refreshToken,
        }

    def refresh_token(self, refresh_token: str):
        stored_token = self.refresh_token_service.get_valid_token(refresh_token)

        if stored_token is None:
            return None

        self.refresh_token_service.revoke_token(refresh_token)

        new_refresh_token = self.refresh_token_service.create_token(
            stored_token.user_id
        )
        access_token = create_access_token(stored_token.user_id)

        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
        }

    def logout(self, user_id: int, refresh_token: str):
        user = self.repository.get_by_id(user_id)
        if user is None:
            return None

        self.refresh_token_service.revoke_token(refresh_token)

    def logout_all(self, user_id: int):
        user = self.repository.get_by_id(user_id)
        if user is None:
            return None

        self.refresh_token_service.revoke_all(user_id)
