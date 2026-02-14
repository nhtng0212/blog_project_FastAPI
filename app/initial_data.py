from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.blog import User, UserRole
from app.core.security import get_password_hash 

def create_admin():
    db = SessionLocal()
    admin = db.query(User).filter(User.email == "admin@gmail.com").first()
    if not admin:
        admin_obj = User(
            email="admin@gmail.com",
            hashed_password=get_password_hash("admin123"),
            full_name="System Admin",
            role=UserRole.ADMIN,
            is_active=True
        )
        db.add(admin_obj)
        db.commit()
        print("Admin account created successfully!")
    else:
        print("Admin account already exists.")
    db.close()

if __name__ == "__main__":
    create_admin()