import boto3
import logging
from botocore.exceptions import ClientError
from app.core.config import settings

# Khởi tạo S3 Client
s3_client = boto3.client(
    "s3",
    endpoint_url="http://localstack:4566" if settings.DEBUG else None,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_S3_REGION,
)


def generate_presigned_url(object_name,file_type, expiration=3600):
    """Tạo link để Client tự upload file lên S3"""
    try:
        response = s3_client.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": settings.AWS_S3_BUCKET_NAME,
                "Key": object_name,
                "ContentType": file_type,
            },
            ExpiresIn=expiration,
        )
        return response
    except Exception as e:
        print(f"Error generating pre-signed URL: {e}")
        return None


# def upload_file_to_s3(file_obj, object_name, content_type):
#     """
#     Upload file lên S3 , trả về URL công khai
#     - file_obj: Dữ liệu file
#     - object_name: Đường dẫn lưu trên S3
#     - content_type: Định dạng file
#     """
#     try:
#         s3_client.upload_fileobj(
#             file_obj,
#             settings.AWS_S3_BUCKET_NAME,
#             object_name,
#             ExtraArgs={
#                 "ACL": "public-read",
#                 "ContentType": content_type
#             }
#         )

#         # Tạo URL trả về
#         url = f"https://{settings.AWS_S3_BUCKET_NAME}.s3.{settings.AWS_S3_REGION}.amazonaws.com/{object_name}"
#         return url
#     except ClientError as e:
#         logging.error(f"S3 Upload Error: {e}")
#         return None
