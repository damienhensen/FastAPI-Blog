from datetime import datetime, timedelta, timezone
import os

import base64
import hashlib

import bcrypt
import jwt


def hash_password(password: str) -> str:
    password = _prepare_password(password)

    return bcrypt.hashpw(password, bcrypt.gensalt()).decode()


def verify_password(password: str, hash: str) -> bool:
    password = _prepare_password(password)

    return bcrypt.checkpw(password, hash.encode())


def _prepare_password(password: str) -> str:
    return base64.b64encode(hashlib.sha256(password.encode()).digest())


def create_access_token(user_id: int, user_email: str) -> str:
    expiry_time = int(os.getenv("JWT_EXPIRES_MINUTES", 15))
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=expiry_time)
    data = {"sub": str(user_id), "email": user_email, "exp": expires_at}

    return jwt.encode(
        data, os.getenv("JWT_SECRET_KEY"), algorithm=os.getenv("JWT_ALGORITHM", "HS256")
    )
