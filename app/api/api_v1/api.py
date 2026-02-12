from fastapi import APIRouter
from app.api.api_v1.endpoints import auth

api_router = APIRouter()

# Đăng ký model con
api_router.include_router(auth.router, prefix="/auth",tags=["auth"])
