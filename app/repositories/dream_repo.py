# app/repositories/dream_repo.py
from typing import Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, func
from app.models.dream import Dream
from app.models.like import Like
from app.models.comment import Comment
from app.repositories.base import Repository


class DreamRepository(Repository[Dream]):
    def __init__(self):
        super().__init__(Dream)

    def list_by_author_and_category(
        self,
        db: Session,
        author_id: Optional[int] = None,
        category_id: Optional[int] = None,
        offset: int = 0,
        limit: int = 50
    ):
        likes_count = (
            select(func.count(Like.id))
            .where(Like.dream_id == Dream.id)
            .correlate(Dream)
            .scalar_subquery()
        )

        comments_count = (
            select(func.count(Comment.id))
            .where(Comment.dream_id == Dream.id)
            .correlate(Dream)
            .scalar_subquery()
        )
        stmt = (
            select(Dream,likes_count.label("likes_count"), comments_count.label("comments_count"))
            .options(joinedload(Dream.author), joinedload(Dream.category),joinedload(Dream.likes))
        )

        #  add filters dynamically
        if author_id:
            stmt = stmt.where(Dream.author_id == author_id)
        if category_id:
            stmt = stmt.where(Dream.category_id == category_id)

        stmt = stmt.offset(offset).limit(limit)
        return db.execute(stmt).unique().all()