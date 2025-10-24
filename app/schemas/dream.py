# app/schemas/dream.py
from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from typing import Optional


class DreamBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)


class DreamCreate(DreamBase):
    pass


class DreamUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    content: Optional[str] = Field(default=None, min_length=1)
    image_url: Optional[str] = None
    is_public: Optional[bool] = None
    tags: Optional[list[str]] = None


class DreamRead(DreamBase):
    id: int
    image_url: Optional[str] = None
    ai_image_url: Optional[str] = None
    author_id: int
    author_name: Optional[str] = None 
    category_name: Optional[str] = None 
    likes_count: int = 0       # new
    comments_count: int = 0    # new
    is_liked_by_user: bool = False
    created_at: datetime
    updated_at: datetime


class Config:
    from_attributes = True