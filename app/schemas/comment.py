# app/schemas/comment.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class CommentBase(BaseModel):
    content: str = Field(min_length=1)


class CommentCreate(CommentBase):
    dream_id: int


class CommentRead(CommentBase):
    id: int
    dream_id: int
    author_id: int
    created_at: datetime


class Config:
    from_attributes = True