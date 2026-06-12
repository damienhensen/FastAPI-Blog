from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.refresh_token import RefreshToken


class RefreshTokenRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_user_id(self, user_id: int):
        return (
            self.db.query(RefreshToken)
            .filter(RefreshToken.user_id == user_id)
            .filter(RefreshToken.expires_at > datetime.now(timezone.utc))
            .filter(RefreshToken.revoked_at.is_(None))
            .all()
        )

    def get_active_by_selector(self, selector: str):
        return (
            self.db.query(RefreshToken)
            .filter(RefreshToken.selector == selector)
            .filter(RefreshToken.expires_at > datetime.now(timezone.utc))
            .filter(RefreshToken.revoked_at.is_(None))
            .first()
        )

    def create(self, refresh_token: RefreshToken):
        self.db.add(refresh_token)
        self.db.commit()
        self.db.refresh(refresh_token)
        return refresh_token

    def commit(self):
        self.db.commit()
