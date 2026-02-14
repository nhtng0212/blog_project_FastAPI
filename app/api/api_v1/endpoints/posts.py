from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api import deps
from app.db.session import get_db
from app.schemas.post import PostOut, PostCreate
from app.services.post_service import post_service
from app.core.redis import redis_client
from app.schemas.utils import Page
import json
from app.core.config import settings
from fastapi.encoders import jsonable_encoder

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
    cache_key = f"post_list_p{page}_s{size}"
    
    # Lấy thử từ Redis trước
    cached_data = redis_client.get(cache_key)
    if cache_key:
        return json.loads(cached_data)
    
    # Không có từ Redis, query
    items, total = post_service.get_multi_with_total(db, page=page, size=size)
    result = {
        "items": items,
        "total": total,
        "page": page,
        "size": size
    }
    
    # Lưu vào Redis
    redis_client.setex(
        cache_key,
        settings.POST_EXPIRE_HOURS,
        json.dumps(jsonable_encoder(result))
    )
    
    return result

@router.get("/tag/{tag_name}", response_model=Page[PostOut])
def list_posts_by_tag(
    tag_name: str,
    db: Session = Depends(get_db),
    page: int = 1,
    size: int = 10
):
    cache_key = f"post_list_tag_{tag_name}_p{page}_s{size}"
    
    cached_data = redis_client.get(cache_key)
    # Lấy từ Redis nếu có
    if cache_key:
        return json.loads(cached_data)
    
    # Nếu không có từ Redis thì query
    items, total = post_service.get_multi_with_total(
        db, tag_name=tag_name, page=page, size=size
    )
    result = {"items": items, "total": total, "page": page, "size": size}
    
    # Lưu lại cho lần sau
    redis_client.setex(cache_key, 3600, json.dumps(jsonable_encoder(result)))
    
    return result