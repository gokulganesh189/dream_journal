# app/repositories/base.py
"""Base repository with common helpers.
- SRP: Reusable DB helpers only.
- OCP: Extend for new entities without changing this file.
"""
from typing import Generic, TypeVar, Type
from sqlalchemy.orm import Session

T = TypeVar("T")

class Repository(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model
    def get(self, db: Session, id: int) -> T | None:
        return db.get(self.model, id)
    def list(self, db: Session, offset: int = 0, limit: int = 50):
        return db.query(self.model).offset(offset).limit(limit).all()
    def add(self, db: Session, obj: T) -> T:
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj
    def delete(self, db: Session, obj: T) -> None:
        db.delete(obj)
        db.commit()