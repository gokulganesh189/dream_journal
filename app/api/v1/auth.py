from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.services.auth_service import AuthService
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserCreate, UserRead, Token


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead)
def register(data: UserCreate, db: Session = Depends(get_db)):
    service = AuthService(UserRepository())
    return service.register(db, data)


@router.post("/login", response_model=Token)
def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    service = AuthService(UserRepository())
    token = service.login(db, email=email, password=password)
    return {"access_token": token, "token_type": "bearer"}