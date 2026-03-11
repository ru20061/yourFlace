from sqlalchemy import Column, BigInteger, String, Integer, Boolean, Text, TIMESTAMP, Date, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func
from app.database import Base

class CelebVideoComment(Base):
    __tablename__ = "celeb_video_comments"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    celeb_video_id = Column(BigInteger, ForeignKey('celeb_videos.id'), nullable=False)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    parent_comment_id = Column(BigInteger, ForeignKey('celeb_video_comments.id'), nullable=True)
    content = Column(Text, nullable=False)
    commenter_role = Column(String(20), nullable=False)
    status = Column(String(20), default='active', nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
