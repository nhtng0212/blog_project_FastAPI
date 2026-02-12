import uuid
from sqlalchemy import Column, String, Text, ForeignKey, Boolean, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.db.base_class import Base

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"
    
class User(Base):
    id = Column(UUID(as_uuid=True), primary_key=True,default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    avatar_url = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(UserRole), default=UserRole.USER)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Quen hệ
    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")
    
class Post(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, index=True, nullable=False)
    image_url = Column(String, nullable=True)
    video_url = Column(String, nullable=True)
    content = Column(Text, nullable=False)
    author_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Quan hệ
    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    
class Comment(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = Column(Text, nullable=False)
    post_id = Column(UUID(as_uuid=True), ForeignKey("post.id"))
    author_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    image_url = Column(String, nullable=True)
    video_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Quan hệ
    post = relationship("Post", back_populates="comments")
    author = relationship("User")
    
    