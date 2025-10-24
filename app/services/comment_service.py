# app/services/comment_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.comment_repo import CommentRepository
from app.models.comment import Comment
from app.schemas.comment import CommentCreate


class CommentService:
    def __init__(self, comments: CommentRepository):
        self.comments = comments


    def add(self, db: Session, author_id: int, data: CommentCreate) -> Comment:
        comment = Comment(content=data.content, dream_id=data.dream_id, author_id=author_id)
        return self.comments.add(db, comment)


    def delete(self, db: Session, comment_id: int, author_id: int) -> None:
        comment = self.comments.get(db, comment_id)
        if not comment or comment.author_id != author_id:
            raise HTTPException(status_code=404, detail="Comment not found or unauthorized")
        self.comments.delete(db, comment)