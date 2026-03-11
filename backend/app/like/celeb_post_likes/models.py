from sqlalchemy import Column, BigInteger, String, Integer, Boolean, Text, TIMESTAMP, Date, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func
from app.database import Base

class CelebPostLike(Base):
    __tablename__ = "celeb_post_likes"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    celeb_id = Column(BigInteger, ForeignKey('celebs.id'), nullable=False)
    post_id = Column(BigInteger, ForeignKey('posts.id'), nullable=False)
    search_text = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
