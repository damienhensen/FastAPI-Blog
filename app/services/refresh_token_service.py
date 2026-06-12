from datetime import datetime, timedelta, timezone
import secrets

from app.core.security import hash_password, verify_password
from app.models.refresh_token import RefreshToken
from app.repositories.refresh_token_repository import RefreshTokenRepository


class RefreshTokenService:
    def __init__(self, repository: RefreshTokenRepository):
        self.repository = repository

    def get_valid_token(self, refresh_token: str):
        selector, secret = refresh_token.split(".", 1)

        stored_token = self.repository.get_active_by_selector(selector)

        if stored_token is None:
            return None

        if not verify_password(secret, stored_token.token):
            return None

        return stored_token

    def create_token(self, user_id: int) -> str:
        expires_at = datetime.now(timezone.utc) + timedelta(days=30)

        selector = secrets.token_urlsafe(32)
        secret = secrets.token_urlsafe(64)

        refresh_token = RefreshToken(
            user_id=user_id,
            selector=selector,
            token=hash_password(secret),
            expires_at=expires_at,
        )

        self.repository.create(refresh_token)

        return f"{selector}.{secret}"

    def revoke_token(self, refresh_token: str) -> bool:
        try:
            selector, secret = refresh_token.split(".", 1)
        except ValueError:
            return False

        stored_token = self.repository.get_active_by_selector(selector)

        if stored_token is None:
            return False

        if not verify_password(secret, stored_token.token):
            return False

        stored_token.revoked_at = datetime.now(timezone.utc)
        self.repository.commit()

        return True

    def revoke_all(self, user_id: int):
        tokens = self.repository.get_by_user_id(user_id)

        for token in tokens:
            token.revoked_at = datetime.now(timezone.utc)

        self.repository.commit()
