from sqlalchemy.orm import Session
from app.models.blog import User, Post, Comment, PostStatus
from app.core.redis import redis_client
from uuid import UUID

class AdminService:
    @staticmethod
    def approve_post(db: Session, post_id: UUID):
        post = db.query(Post).filter(Post.id == post_id).first()
        if post:
            post.status = PostStatus.APPROVED
            db.commit()
            db.refresh(post)
            # Xóa cache danh sách bài viết công khai để bài mới xuất hiện
            keys = redis_client.keys("posts_list_*")
            if keys:
                redis_client.delete(*keys)
        return post

    @staticmethod
    def ban_user(db: Session, user_id: UUID):
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.is_active = False
            db.commit()
            # Đưa User vào blacklist
            redis_client.delete(f"user_profile:{user_id}")
        return user

    @staticmethod
    def delete_any_comment(db: Session, comment_id: UUID):
        comment = db.query(Comment).filter(Comment.id == comment_id).first()
        if comment:
            post_id = comment.post_id
            db.delete(comment)
            db.commit()
            # Xóa cache comment của bài viết
            keys = redis_client.keys(f"comments:post:{post_id}:*")
            if keys:
                redis_client.delete(*keys)
        return True

admin_service = AdminService()