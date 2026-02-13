from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.api import deps
from app.db.session import get_db
from app.models.blog import Post, User, Comment, PostStatus
from app.schemas.post import PostOut
from app.schemas.user import UserOut

router = APIRouter(dependencies=[Depends(deps.get_current_admin)])

# Quản lý bài viết
@router.patch("/posts/{post_id}/approve", response_model=PostOut)
def approve_post(post_id: UUID, db: Session = Depends(get_db)):
    """Duyệt bài viết để hiển thị công khai"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    post.status = PostStatus.APPROVED
    db.commit()
    db.refresh(post)
    
    # Cache
    from app.core.redis import redis_client
    keys = redis_client.keys("posts_list_*")
    if keys:
        redis_client.delete(*keys)
    
    return post

@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def admin_delete_post(post_id: UUID, db: Session = Depends(get_db)):
    """Admin có quyền xóa bất kỳ bài viết nào vi phạm"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return None

# Quản lý người dùng
@router.get("/user", response_model=List[UserOut])
def list_user_for_admin(db: Session = Depends(get_db), page: int = 1, size: int=10):
    """Admin xem danh sách toàn bộ người dùng để quản lý"""
    if page < 1: page = 1
    if size > 100: size = 100
    skip = (page - 1) * size
    limit = size
    
    return db.query(User).offset(skip).limit(limit).all()

@router.delete("/users/{user_id}")
def ban_user(user_id: UUID, db:Session = Depends(get_db)):
    """Admin có thể khóa tài khoản người dùng"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = False
    db.commit()
    return {"detail": "User has been banned"}