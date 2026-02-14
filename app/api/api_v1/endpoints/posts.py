from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api import deps
from app.db.session import get_db
from app.schemas.post import PostOut, PostCreate
from app.services.post_service import post_service
from app.core.redis import redis_client
from app.schemas.utils import Page

router = APIRouter()

@router.post("/", response_model=PostOut, status_code=status.HTTP_201_CREATED)
def create_post(
    *,
    db: Session = Depends(get_db),
    post_in: PostCreate,
    current_user = Depends(deps.get_current_user)
):
    """Tạo bài viết mới. Xóa cache danh sách bài viết sau khi tạo"""
    post = post_service.create(db, obj_in=post_in, author_id=current_user.id)

    # Xóa toàn bộ cache bài viết cũ để thấy bài viết mới ngay
    keys = redis_client.keys("post_list_*")
    if keys:
        redis_client.delete(*keys)
        
    return post

@router.get("/", response_model=Page[PostOut])
def list_posts(db: Session = Depends(get_db), page: int = 1, size: int = 10):
    """Lấy danh sách bài viết"""
    items, total = post_service.get_multi_with_total(db, page=page, size=size)
    
    return {
        "items": items,
        "total": total,
        "page": page,
        "size": size
    }

@router.get("/tag/{tag_name}", response_model=Page[PostOut])
def list_posts_by_tag(
    tag_name: str,
    db: Session = Depends(get_db),
    page: int = 1,
    size: int = 10
):
    items, total = post_service.get_multi_with_total(
        db, tag_name=tag_name, page=page, size=size
    )
    return {"items": items, "total": total, "page": page, "size": size}