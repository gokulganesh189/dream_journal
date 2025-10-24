from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user_id
from app.services.like_service import LikeService
from app.repositories.like_repo import LikeRepository


router = APIRouter(prefix="/likes", tags=["likes"])


like_service = LikeService(LikeRepository())


@router.post("/{dream_id}/toggle")
def toggle_like(dream_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    liked, count = like_service.toggle(db, user_id, dream_id)
    return {"liked": liked, "count": count}