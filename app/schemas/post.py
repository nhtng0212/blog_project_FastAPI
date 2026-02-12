from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from app.schemas.user import UserShort

#
class PostBase(BaseModel):
    title: str
    content: str
    image_url: Optional[str] = None
    video_url: Optional[str] = None
    
# Tạo bài viết
class PostCreate(PostBase):
    pass

# Cập nhật bài viết
class PostUpdate(PostBase):
    title: Optional[str] = None
    content: Optional[str] = None
    
# Trả về cho Client
class PostOut(PostBase):
    id: UUID
    author_id: UUID
    author: UserShort
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    # Cho phép Pydantic đọc dữ liệu từ SQLAIchemy Model
    model_config = ConfigDict(from_attributes=True)