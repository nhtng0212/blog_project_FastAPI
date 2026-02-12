from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Tạo engine kết nối
engine = create_engine(settings.DATABASE_URL)

# Mỗi request, tạo 1 session
SessionLocal = sessionmaker(autocomit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()