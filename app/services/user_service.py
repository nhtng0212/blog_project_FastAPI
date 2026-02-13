from sqlalchemy.orm import Session
from app.models.blog import User
from app.schemas.user import UserCreate, UserUpdate, UserRole
from app.core.security import get_password_hash, verify_password

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
            hashed_password=get_password_hash(str(obj_in.password)),
            full_name=obj_in.full_name,
            avatar_url=obj_in.avatar_url,
            bio=obj_in.bio,
            role=UserRole.USER,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    @staticmethod
    def authenticate(db: Session, email: str, password: str):
        """Xác thực người dùng bằng email và mật khẩu"""
        user = UserService.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
    
    @staticmethod
    def update(db: Session, db_obj: User, obj_in: UserUpdate):
        update_data = obj_in.model_dump(exclude_unset=True)    

        if update_data.get("password"):
            # Nếu đổi pass thì hash lại
            hashed_password = get_password_hash(update_data["password"])
            db_obj.hashed_password = hashed_password
            del update_data["password"]
            
        # Cập nhật các trường còn lại
        for field in update_data:
            if hasattr(db_obj, field):
                setattr(db_obj, field, update_data[field])
                
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
        
# Khởi tạo để dùng ở Router
user_service = UserService()