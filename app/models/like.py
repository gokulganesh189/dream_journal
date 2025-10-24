# app/models/like.py
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey, UniqueConstraint, DateTime, func
from app.db.session import Base


class Like(Base):
    __tablename__ = "likes"
    __table_args__ = (UniqueConstraint("user_id", "dream_id", name="uq_user_dream_like"),)


    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    dream_id: Mapped[int] = mapped_column(ForeignKey("dreams.id", ondelete="CASCADE"))
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())


    user = relationship("User", back_populates="likes")
    dream = relationship("Dream", back_populates="likes")