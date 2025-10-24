# app/schemas/like.py
from pydantic import BaseModel
from datetime import datetime


class LikeRead(BaseModel):
    id: int
    user_id: int
    dream_id: int
    created_at: datetime


class Config:
    from_attributes = True