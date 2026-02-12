from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.schemas.user import UserShort

class CommentBase(BaseModel):
    content: str
    imgae_url: Optional[str] = True
    video_url: Optional[str] = True
    
# Tạo comment
class CommentCreate(CommentBase):
    post_id: UUID
    
# Chỉnh sửa comment
class CommentUpdate(CommentBase):
    content: str
    
# Trả về cho Client
class CommentOut(CommentBase):
    id: UUID
    post_id: UUID
    author_id: UUID
    author: UserShort
    created_at: datetime
    update_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)