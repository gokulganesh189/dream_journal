# app/repositories/comment_repo.py
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.comment import Comment
from app.repositories.base import Repository


class CommentRepository(Repository[Comment]):
    def __init__(self):
        super().__init__(Comment)
    def list_for_dream(self, db: Session, dream_id: int):
        return db.execute(select(Comment).where(Comment.dream_id == dream_id)).scalars().all()