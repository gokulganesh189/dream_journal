# app/repositories/like_repo.py
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from app.models.like import Like
from app.repositories.base import Repository


class LikeRepository(Repository[Like]):
    def __init__(self):
        super().__init__(Like)

    def get_by_user_and_dream(self, db: Session, user_id: int, dream_id: int) -> Like | None:
        stmt = select(Like).where(and_(Like.user_id == user_id, Like.dream_id == dream_id))
        return db.execute(stmt).scalar_one_or_none()