"""FastAPI application factory.
- SRP: App setup and router registration only.
- OCP: New routers mountable without changing core code.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.session import engine, Base
from app.api.v1 import auth as auth_router
from app.api.v1 import dreams as dreams_router
from app.api.v1 import comments as comments_router
from app.api.v1 import likes as likes_router
from app.middleware.logging_middleware import RequestResponseLoggingMiddleware

# # Create tables if not using Alembic (demo convenience)
# Base.metadata.create_all(bind=engine)


app = FastAPI(title=settings.app_name)

app.add_middleware(RequestResponseLoggingMiddleware)


app.add_middleware(
CORSMiddleware,
allow_origins=["*"], allow_credentials=True,
allow_methods=["*"], allow_headers=["*"],
)


api = settings.api_v1_str
app.include_router(auth_router.router, prefix=api)
app.include_router(dreams_router.router, prefix=api)
app.include_router(comments_router.router, prefix=api)
app.include_router(likes_router.router, prefix=api)


@app.get("/")
async def root():
    return {"name": settings.app_name, "version": 1}