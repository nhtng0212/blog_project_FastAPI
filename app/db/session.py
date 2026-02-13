from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
import boto3

# Tạo engine kết nối
engine = create_engine(settings.DATABASE_URL)

# Mỗi request, tạo 1 session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def init_local_s3():
    # Kết nối tới LocalStack (4566)
    s3 = boto3.client(
        "s3",
        endpoint_url="http://localstack:4566",
        aws_access_key_id="test",
        region_name="ap-southeast-1"
    )
    try:
        s3.create_bucket(
            Bucket=settings.AWS_S3_BUCKET_NAME,
            CreateBucketConfiguration={'LocationConstraint':'ap-southeast-1'}
        )
        print(f"Successfully created bucket: {settings.AWS_S3_BUCKET_NAME}")
    except Exception as e:
        print(f"Bucket might exist or error: {e}")