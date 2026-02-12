from fastapi import APIRouter
from app.api.api_v1.endpoints import auth, comments, media, posts

api_router = APIRouter()

# Đăng ký model con
api_router.include_router(auth.router, prefix="/auth",tags=["auth"])
api_router.include_router(media.router, prefix="/media", tags=["media"])