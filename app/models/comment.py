# app/models/comment.py
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Text, ForeignKey, DateTime, func
from app.db.session import Base


class Comment(Base):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)


    dream_id: Mapped[int] = mapped_column(ForeignKey("dreams.id", ondelete="CASCADE"))
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))


    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())


    dream = relationship("Dream", back_populates="comments")
    author = relationship("User", back_populates="comments")