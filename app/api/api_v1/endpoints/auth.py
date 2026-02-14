from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import UserOut, UserCreate
from app.services.user_service import user_service

from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import create_access_token, create_refresh_token
from app.schemas.user import Token
from app.api import deps
from app.core.config import settings

from jose import jwt, JWTError

from app.models.blog import User

from app.core.redis import redis_client

router = APIRouter()

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate
) -> Any:
    """
    Đăng ký người dùng mới
    """
    
    # Kiểm tra email tồn tại chưa
    user = user_service.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system"
        )
    
    # Tạo user mới
    return user_service.create(db, obj_in=user_in)

@router.post("/login", response_model=Token)
def login(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    Đăng nhập lấy JWT Access Token.
    * from_data.username là email
    """
    user = user_service.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    
    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    redis_client.setex(
        f"refresh_token:{user.id}",
        timedelta(days=settings.REFRSH_TOKEN_EXPIRE_DAYS),
        refresh_token
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }
    
@router.post("/refresh-token", response_model=Token)
def refresh_token(refresh_token: str, db: Session = Depends(get_db)) -> Any:
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=400, detail="Invalid token type")
        user_id = payload.get("sub")
    except jwt.JWTError:
        raise HTTPException(status_code=403, detail="Refresh token expired on invalid")
    
    # Kiểm tra Redis trước
    stored_token = redis_client.get(f"refresh_token:{user_id}")
    if not stored_token:
        raise HTTPException(status_code=401, detail="Refresh token has expired or been revoked")

    if stored_token.decode("utf-8") != refresh_token:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=404, detail="User not found or inactive")
    
    # Tạo access token mới
    new_access_token = create_access_token(user.id)
    return {
        "access_token": new_access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }
    
@router.post("/logout")
def logout(
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Đăng xuất, xóa Refresh Token khỏi Redis
    """
    # Xóa token của user hiện tại trong Redis
    redis_client.delete(f"refresh_token:{current_user.id}")
    
    return {"detail": "Successfully logged out"}