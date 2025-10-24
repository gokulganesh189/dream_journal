# app/services/like_service.py
from sqlalchemy.orm import Session
from app.repositories.like_repo import LikeRepository
from app.models.like import Like


class LikeService:
    def __init__(self, likes: LikeRepository):
        self.likes = likes


    def toggle(self, db: Session, user_id: int, dream_id: int) -> tuple[bool, int]:
        """Toggle like; returns (is_liked_now, total_count)."""
        existing = self.likes.get_by_user_and_dream(db, user_id, dream_id)
        if existing:
            self.likes.delete(db, existing)
            count = db.query(Like).filter(Like.dream_id == dream_id).count()
            return (False, count)
        like = Like(user_id=user_id, dream_id=dream_id)
        self.likes.add(db, like)
        count = db.query(Like).filter(Like.dream_id == dream_id).count()
        return (True, count)