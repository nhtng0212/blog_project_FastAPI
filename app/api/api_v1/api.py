from fastapi import APIRouter
from app.api.api_v1.endpoints import admin,auth, users,comments, media, posts

api_router = APIRouter()

# Đăng ký model con
api_router.include_router(auth.router, prefix="/auth",tags=["auth"])
api_router.include_router(admin.router, prefix="/admin",tags=["admin"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(posts.router, prefix="/posts", tags=["posts"])
api_router.include_router(comments.router, prefix="/comments",tags=["comments"])
api_router.include_router(media.router, prefix="/media", tags=["media"])