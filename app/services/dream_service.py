# app/services/dream_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import Optional, List
from app.repositories.dream_repo import DreamRepository
from app.repositories.like_repo import LikeRepository
from app.models.dream import Dream
from app.schemas.dream import DreamCreate, DreamUpdate, DreamRead



class DreamService:
    def __init__(self, dreams: DreamRepository, likes: LikeRepository):
        self.dreams = dreams
        self.likes = likes


    def create(self, db: Session, author_id: int, data: DreamCreate, image_url: Optional[str] = None, ai_image_url: Optional[str] = None) -> Dream:
        dream = Dream(title=data.title, content=data.content, author_id=author_id, image_url=image_url, ai_image_url=ai_image_url)
        return self.dreams.add(db, dream)


    def update(self, db: Session, dream_id: int, author_id: int, update_data: dict) -> Dream:
        dream = self.dreams.get(db, dream_id)
        if not dream or dream.author_id != author_id:
            raise HTTPException(status_code=404, detail="Dream not found or unauthorized")

        for key, value in update_data.items():
            setattr(dream, key, value)

        db.commit()
        db.refresh(dream)
        return dream


    def delete(self, db: Session, dream_id: int, author_id: int) -> None:
        dream = self.dreams.get(db, dream_id)
        if not dream or dream.author_id != author_id:
            raise HTTPException(status_code=404, detail="Dream not found or unauthorized")
        self.dreams.delete(db, dream)
        
    def list_dreams(self, db: Session, user_id: Optional[int] = None) -> List[DreamRead]:
        """Retrieve dreams and enrich with author_name."""
        dreams = self.dreams.list_by_author_and_category(db)
        result = []
        for dream,likes_count,comments_count in dreams:
            schema_obj = DreamRead.model_validate(dream, from_attributes=True)
            schema_obj.author_name = dream.author.username if dream.author else None
            schema_obj.category_name = dream.category.name if dream.category else None
            schema_obj.likes_count = likes_count
            schema_obj.comments_count = comments_count
            if user_id:
                like = self.likes.get_by_user_and_dream(db, dream.id, user_id)
                schema_obj.is_liked_by_user = bool(like)
            result.append(schema_obj)
        return result