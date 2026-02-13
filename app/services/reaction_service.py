from app.core.redis import redis_client
from sqlalchemy.orm import Session
from app.models.blog import PostReaction

class ReactionService:
    @staticmethod
    def toggle_post_reaction(db: Session, post_id:str, user_id:str, reaction_type:str):
        # Kiểm tra đã react chưa
        existing = db.query(PostReaction).filter_by(post_id=post_id, user_id=user_id).first()
        cache_key = f"post_reactions_count:{post_id}"
        
        # Nếu đã có reaction
        if existing:
            # Nếu trùng type thì là Un-reaction
            if existing.type == reaction_type:
                db.delete(existing)
                db.commit()
                redis_client.decr(cache_key)
                return {"action": "unreacted"}
            else:
                existing.type = reaction_type
                db.commit()
                return {"action": "changed"}
            
        # Tạo mới reaction
        new_reaction = PostReaction(post_id=post_id, user_id=user_id, type=reaction_type)
        db.add(new_reaction)
        db.commit()
        
        # Tăng count
        redis_client.incr(cache_key)
        return {"action": "reacted"}
    
    @staticmethod
    def get_reaction_count(db: Session, post_id: str):
        cache_key = f"post_reactions_count:{post_id}"
        count = redis_client.get(cache_key)
        
        if count is None:
            count = db.query(PostReaction).filter_by(post_id=post_id).count()
            redis_client.set(cache_key, count, ex=3600) 
            
        return int(count)