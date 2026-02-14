import json 
from sqlalchemy.orm import Session
from app.models.blog import Post, PostStatus
from app.schemas.post import PostCreate, PostOut
from app.core.redis import get_cache, set_cache
from uuid import UUID
from app.models.blog import Tag

class PostSerivce:
    @staticmethod
    def create(db: Session, obj_in: PostCreate, author_id: UUID):
        # Lấy danh sách tag
        tag_names = obj_in.tags if obj_in.tags else []
        db_tags = []
        
        # Chuyển tags thành Object Tag
        for name in tag_names:
            name = name.lower().strip()
            tag_obj = db.query(Tag).filter(Tag.name == name).first()
            if not tag_obj:
                tag_obj = Tag(name=name)
                db.add(tag_obj)
            db_tags.append(tag_obj)
            
        # Tạo Post
        post_data = obj_in.model_dump()
        post_data.pop("tags") 
        
        db_obj = Post(
            **post_data,
            author_id=author_id,
            tags=db_tags 
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    @staticmethod
    def get_multi_with_total(
        db: Session, 
        *, 
        status: str = None, 
        tag_name: str = None, 
        page: int = 1, 
        size: int = 10
    ):
        if page < 1: page = 1
        skip = (page - 1) * size
        
        query = db.query(Post)
        
        # Lọc theo Status
        if status:
            target_status = status.lower().strip()
            query = query.filter(Post.status == target_status)
        else:
            query = query.filter(Post.status == PostStatus.APPROVED)
            
        # Lọc theo Tag
        if tag_name:
            clean_tag = tag_name.lower().strip()
            tag_exists = db.query(Tag).filter(Tag.name == clean_tag).first()
            if not tag_exists:
                return [], 0
            query = query.join(Post.tags).filter(Tag.name == clean_tag)

        total = query.count()
        
        # Lấy dữ liệu phân trang
        items = query.order_by(Post.created_at.desc())\
                    .offset(skip)\
                    .limit(size)\
                    .all()
        
        return items, total
    
    
post_service = PostSerivce()
 
        