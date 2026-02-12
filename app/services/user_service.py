from sqlalchemy.orm import Session
from app.models.blog import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

class UserService:
    @staticmethod
    def get_by_email(db: Session, email: str):
        """Tìm người dùng theo email"""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def create(db: Session, obj_in: UserCreate):
        """Tạo người dùng mới"""
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            role=obj_in.role,
        )
        db.add(obj_in)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
# Khởi tạo để dùng ở Router
user_service = UserService()