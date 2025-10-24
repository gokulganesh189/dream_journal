# app/services/auth_service.py
"""Authentication service.
- SRP: Auth flows only (register/login/token verify).
- DIP: Uses UserRepository abstraction and security helpers.
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.schemas.user import UserCreate
from app.models.user import User
from app.repositories.user_repo import UserRepository
from app.core.security import get_password_hash, verify_password, create_access_token


class AuthService:
    def __init__(self, users: UserRepository):
        self.users = users


    def register(self, db: Session, data: UserCreate) -> User:
        if self.users.get_by_email(db, data.email):
            raise HTTPException(status_code=400, detail="Email already registered")
        if self.users.get_by_username(db, data.username):
            raise HTTPException(status_code=400, detail="Username already taken")
        user = User(email=data.email, username=data.username, hashed_password=get_password_hash(data.password))
        return self.users.add(db, user)


    def login(self, db: Session, email: str, password: str) -> str:
        user = self.users.get_by_email(db, email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        return create_access_token(subject=user.id, extra={"username": user.username})