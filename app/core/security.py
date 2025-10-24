"""Security helpers for hashing and JWT tokens.
- SRP: Crypto + token utilities only.
- OCP: Algorithms/claims extendable without modifying users of this module.
"""
from datetime import datetime, timedelta, timezone
from typing import Any, Optional
import hashlib
import jwt
from passlib.context import CryptContext
from app.core.config import settings

# Use bcrypt for password hashing
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def create_access_token(
    subject: str | int,
    expires_minutes: Optional[int] = None,
    extra: Optional[dict[str, Any]] = None
) -> str:
    """Create a JWT access token with optional extra claims."""
    expire = datetime.now(tz=timezone.utc) + timedelta(
        minutes=expires_minutes or settings.access_token_expire_minutes
    )
    to_encode: dict[str, Any] = {"sub": str(subject), "exp": expire}
    if extra:
        to_encode.update(extra)
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def _sha256_pre_hash(password: str) -> str:
    """Pre-hash the password to handle passwords longer than bcrypt's 72-byte limit."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against the stored hash."""
    return pwd_context.verify(_sha256_pre_hash(plain_password), hashed_password)


def get_password_hash(password: str) -> str:
    """Generate a secure hash using SHA256 pre-hash + bcrypt."""
    return pwd_context.hash(_sha256_pre_hash(password))
