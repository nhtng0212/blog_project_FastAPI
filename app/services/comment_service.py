from sqlalchemy.orm import Session
from app.core.redis import redis_client
from app.models.blog import Comment
import json
from app.schemas.comment import CommentCreate
from uuid import UUID

class CommentService:
    @staticmethod
    def create(db: Session, obj_in: CommentCreate, author_id: UUID):
        db_obj = Comment(
            content=obj_in.content,
            post_id=obj_in.post_id,
            author_id=author_id,
            image_url=obj_in.image_url,
            video_url=obj_in.video_url
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    @staticmethod
    def get_by_post_with_paging(db: Session, post_id: UUID, page:int= 1, size: int = 10):
        if page < 1: page = 1
        if size > 100: size = 100
        skip = (page - 1) * size
        limit = size
        
        cache_key = f"comments:post:{post_id}:p:{skip // limit}"
        
        # Lấy từ redis nếu được
        cached = redis_client.get(cache_key)
        if cached:
            data = json.loads(cached)
            return data["items"], data["total"]
        
        query = db.query(Comment).filter(Comment.post_id == post_id)
        total = query.count()
        items = query.order_by(Comment.created_at.desc()).offset(skip).limit(limit).all()
        
        # Chuẩn bị dữ liệu trả về
        from app.schemas.comment import CommentOut
        items_data = [CommentOut.model_validate(i).model_dump(mode='json') for i in items]
        
        # Lưu vào Redis 5 phút
        redis_client.set(cache_key, json.dumps({"items": items_data, "total": total}),ex=300)
        
        return items, total
                    
comment_service = CommentService()