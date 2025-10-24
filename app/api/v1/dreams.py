from typing import Optional
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, Request
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user_id
from app.schemas.dream import DreamCreate, DreamUpdate, DreamRead
from app.services.dream_service import DreamService
from app.services.image_service import ImageService
from app.repositories.dream_repo import DreamRepository
from app.repositories.like_repo import LikeRepository


router = APIRouter(prefix="/dreams", tags=["dreams"])


dream_service = DreamService(DreamRepository(), LikeRepository())
img_service = ImageService()


@router.post("/", response_model=DreamRead)
async def create_dream(
title: str = Form(...),
content: str = Form(...),
image: Optional[UploadFile] = File(None),
db: Session = Depends(get_db),
user_id: int = Depends(get_current_user_id),
):
    image_url = img_service.save_upload(image) if image else None
    data = DreamCreate(title=title, content=content)
    return dream_service.create(db, author_id=user_id, data=data, image_url=image_url)


@router.get("/", response_model=list[DreamRead])
def list_dreams(db: Session = Depends(get_db),
                user_id: int = Depends(get_current_user_id)):
    dreams = dream_service.list_dreams(db, user_id)
    
    if not dreams:  # Check if empty list or None
        raise HTTPException(status_code=404, detail="No dreams found")
    
    return dreams


@router.get("/{dream_id}", response_model=DreamRead)
def get_dream(dream_id: int, db: Session = Depends(get_db)):
    dream = DreamRepository().get(db, dream_id)
    return dream


@router.patch("/{dream_id}", response_model=DreamRead)
async def update_dream(
    dream_id: int,
    request: Request,
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    # Dynamically extract all form fields
    form = await request.form()
    update_data = {k: v for k, v in form.items() if v != ""}

    if image:
        image_url = img_service.save_upload(image)
        update_data["image_url"] = image_url

    return dream_service.update(db, dream_id, user_id, update_data)


@router.delete("/{dream_id}", status_code=204)
def delete_dream(dream_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    dream_service.delete(db, dream_id, user_id)
    return None