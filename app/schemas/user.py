from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.models.blog import UserRole

# Schema chung 
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    is_active: Optional[bool] = True
    role: Optional[UserRole] = UserRole.USER

    model_config = ConfigDict(from_attributes=True) 

# Schema cho việc Đăng ký (Dữ liệu nhận vào)
class UserCreate(UserBase):
    password: str

# Schema Cập nhật thông tin
class UserUpdate(UserBase):
    password: Optional[str] = None

# Schema trả về cho Client 
class UserOut(UserBase):
    id: UUID
    created_at: datetime

# Schema Token 
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None