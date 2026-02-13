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
    def get_multi_with_total(db:Session, page:int = 0, size:int = 10):
        if page < 1: page = 1
        if size > 100: size = 100
        skip = (page - 1) * size
        limit = size
        
        # Lấy tổng số bài viết có trạng thái APPROVED
        total = db.query(Post).filter(Post.status == PostStatus.APPROVED).count()
        
        # Lấy dữ liệu phân trang
        items = db.query(Post).filter(Post.status == PostStatus.APPROVED).offset(skip).limit(limit).all()
        
        return items, total
    
    @staticmethod
    def get_multi(db: Session, page:int = 0, size:int = 10):
        if page < 1: page = 1
        if size > 100: size = 100
        skip = (page - 1) * size
        limit = size
       
        # Lấy Cache nếu có
        cache_key = f"posts_list_{skip}_{limit}"
        cached = get_cache(cache_key)
        if cached:
            return json.load(cached)
        
        # Lấy từ DB
        posts = db.query(Post).offset(skip).limit(limit).all()
        
        # Lưu vào Cache
        posts_data = [PostOut.model_validate(p).model_dump(mode="json") for p in posts]
        set_cache(cache_key, json.dumps(posts_data), expire=60)
        
        return posts
    
post_service = PostSerivce()
 
        