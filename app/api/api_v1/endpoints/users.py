from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.db.session import get_db
from app.schemas.user import UserOut, UserUpdate
from app.models.blog import User
from app.services import user_service

router = APIRouter()

@router.get("/me", response_model=UserOut)
def read_user_me(current_user: User = Depends(deps.get_current_user)):
    """Lấy thông tin profile hiện tại"""
    return current_user

@router.patch("/me", response_model=UserOut)
def update_user_me(
    obj_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    return user_service.update(db, db_obj=current_user, obj_in=obj_in)