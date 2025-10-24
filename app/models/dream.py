# app/models/dream.py
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, ForeignKey, DateTime, func
from app.db.session import Base


class Dream(Base):
    __tablename__ = "dreams"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    image_url: Mapped[str | None] = mapped_column(String(500))
    ai_image_url: Mapped[str | None] = mapped_column(String(500))


    author_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    author = relationship("User", back_populates="dreams")
    
    
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id", ondelete="CASCADE"))
    category = relationship("Category", back_populates="category")
    

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


    comments = relationship("Comment", back_populates="dream", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="dream", cascade="all, delete-orphan")