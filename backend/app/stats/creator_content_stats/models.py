from sqlalchemy import Column, BigInteger, String, Integer, Boolean, Text, TIMESTAMP, Date, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func
from app.database import Base

class CreatorContentStat(Base):
    __tablename__ = "creator_content_stats"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    creator_id = Column(BigInteger, ForeignKey('creators.id'), unique=True, nullable=False)
    post_count = Column(Integer, default=0)
    image_count = Column(Integer, default=0)
    video_count = Column(Integer, default=0)
    fan_like_count = Column(Integer, default=0)
    fan_recommend_count = Column(Integer, default=0)
    last_updated = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
