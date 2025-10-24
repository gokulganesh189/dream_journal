"""SQLAlchemy engine and session factory.
- SRP: DB connectivity.
- DIP: Others receive `Session` via FastAPI dependency.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings
import os


os.makedirs(settings.media_dir, exist_ok=True)


engine = create_engine(
settings.sqlalchemy_database_uri,
connect_args={"check_same_thread": False} if settings.sqlalchemy_database_uri.startswith("sqlite") else {},
)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass

from app.models import dream, user, comment, like, category