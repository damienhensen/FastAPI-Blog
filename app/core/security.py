import base64
import hashlib

import bcrypt


def hash_password(password: str) -> str:
    password = _prepare_password(password)

    return bcrypt.hashpw(password, bcrypt.gensalt()).decode()


def verify_password(password: str, hash: str) -> bool:
    password = _prepare_password(password)

    return bcrypt.checkpw(password, hash.encode())


def _prepare_password(password: str) -> str:
    return base64.b64encode(hashlib.sha256(password.encode()).digest())
