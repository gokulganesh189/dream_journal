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
    pool_pre_ping=True,          # prevents stale connections
    pool_size=5,                 # safe default
    max_overflow=10,
)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass

from app.models import dream, user, comment, like, category