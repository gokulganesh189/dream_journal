from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user_id
from app.schemas.comment import CommentCreate, CommentRead
from app.services.comment_service import CommentService
from app.repositories.comment_repo import CommentRepository


router = APIRouter(prefix="/comments", tags=["comments"])


comment_service = CommentService(CommentRepository())


@router.post("/", response_model=CommentRead)
def add_comment(data: CommentCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    return comment_service.add(db, user_id, data)


@router.delete("/{comment_id}", status_code=204)
def delete_comment(comment_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    comment_service.delete(db, comment_id, user_id)
    return None