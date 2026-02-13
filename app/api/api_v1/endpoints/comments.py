from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.db.session import get_db
from app.schemas.comment import CommentOut, CommentCreate
from app.models.blog import Comment, Post
from app.schemas.utils import Page
from app.services import comment_service
from uuid import UUID

router = APIRouter()


@router.post("/", response_model=CommentOut)
def create_comment(
    *,
    db: Session = Depends(get_db),
    comment_in: CommentCreate,
    current_user=Depends(deps.get_current_user)
):
    """Bình luận vào một bài viết (Hỗ trợ Media URL)"""
    # Kiểm tra bài viết có tồn tại không
    post = db.query(Post).filter(Post.id == comment_in.post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    db_obj = Comment(
        content=comment_in.content,
        post_id=comment_in.post_id,
        author_id=current_user.id,
        image_url=comment_in.imgae_url,
        video_url=comment_in.video_url,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


@router.get("/{post_id}/comments", response_model=Page[CommentOut])
def get_post_comments(
    post_id: UUID, page: int = 1, size: int = 10, db: Session = Depends(get_db)
):
    skip = (page - 1) * size
    items, total = comment_service.get_by_post_with_paging(
        db, post_id=post_id, skip=skip, limit=size
    )
    return {"items": items, "total": total, "page": page, "size": size}
