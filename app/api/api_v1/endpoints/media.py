from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from app.api import deps

# from app.core.aws import upload_file_to_s3
from app.core.config import settings
from app.core.aws import generate_presigned_url
import uuid

router = APIRouter()


@router.get("/presigned-url")
async def get_presigned_url(
    file_name: str, file_type: str, current_user=Depends(deps.get_current_user)
):
    """
    Trả về link để Client tự upload lên S3
    """
    object_name = f"content/{uuid.uuid4()}_{file_name}"
    # Tạo URL từ aws.py
    url = get_presigned_url(object_name, content_type=file_type)

    if not url:
        raise HTTPException(status_code=500, detail="Could not generate URL")

    return {
        "upload_url": url,
        "file_url": f"http://localhost:4566/{settings.AWS_S3_BUCKET_NAME}/{object_name}",
    }


# @router.post("/upload")
# async def upload_media(
#     file: UploadFile = File(...),
#     current_user = Depends(deps.get_current_user)
# ):
#     """
#     Upload file lên S3
#     Trả về URL
#     """
#     # Kiểm tra định dạng
#     allowed_types = ["image/jpeg","image/png","video/mp4", "video/quicktime"]
#     if file.content_type not in allowed_types:
#         raise HTTPException(status_code=400, detail="File type not supported")

#     # Tạo tên file
#     file_ext = file.filename.split(".")[-1]
#     folder = "videos" if "video" in file.content_type else "images"
#     file_name = f"{folder}/{uuid.uuid4()}.{file.ext}"

#     # Upload
#     url = upload_file_to_s3(file.file, file_name, file.content_type)

#     if not url:
#         raise HTTPException(status_code=500, detail="Could not upload file to S3")

#     return {"url": url}
