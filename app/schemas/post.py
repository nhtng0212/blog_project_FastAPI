from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from app.schemas.user import UserShort
from app.models.blog import PostStatus

# Schema trả về cho từng Tag
class TagOut(BaseModel):
    id: UUID
    name: str
    model_config = ConfigDict(from_attributes=True)

class PostBase(BaseModel):
    title: str
    content: str
    image_url: Optional[str] = None
    video_url: Optional[str] = None

class PostCreate(PostBase):
    tags: List[str] = [] 

class PostUpdate(PostBase):
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None
    status: Optional[PostStatus] = None 
    image_url: Optional[str] = None
    video_url: Optional[str] = None

# Schema trả về cho Client
class PostOut(BaseModel):
    id: UUID
    title: str
    content: str
    image_url: Optional[str] = None
    video_url: Optional[str] = None
    author_id: UUID
    author: UserShort
    status: PostStatus 
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    tags: List[TagOut] = [] 
    
    model_config = ConfigDict(from_attributes=True)