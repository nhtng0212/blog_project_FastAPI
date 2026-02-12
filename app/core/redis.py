import redis
from app.core.config import settings

redis_client = redis.Redis(
    host="redis", 
    port=6379,
    db=0,
    decode_responses=True
)

def set_cache(key, value, expire=300):
    redis_client.setex(key, expire, value)

def get_cache(key):
    return redis_client.get(key)