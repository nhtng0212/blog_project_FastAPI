from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.models.blog import UserRole


# Schema chung 
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    is_active: Optional[bool] = True
    role: Optional[UserRole] = UserRole.USER

    model_config = ConfigDict(from_attributes=True) 

# Schema rút gọn
class UserShort(BaseModel):
    id: UUID
    full_name: Optional[str] =None
    avatar_url: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

# Schema cho việc Đăng ký 
class UserCreate(UserBase):
    password: str

# Schema Cập nhật thông tin
class UserUpdate(UserBase):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None

# Schema trả về cho Client 
class UserOut(UserBase):
    id: UUID
    created_at: datetime

# Schema Token 
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None