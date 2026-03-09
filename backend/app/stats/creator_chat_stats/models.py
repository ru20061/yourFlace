from sqlalchemy import Column, BigInteger, String, Integer, Boolean, Text, TIMESTAMP, Date, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func
from app.database import Base

class CreatorChatStat(Base):
    __tablename__ = "creator_chat_stats"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    creator_id = Column(BigInteger, ForeignKey('creators.id'), unique=True, nullable=False)
    chat_subscriber_count = Column(Integer, default=0)
    chat_image_count = Column(Integer, default=0)
    chat_video_count = Column(Integer, default=0)
    chat_attendance_days = Column(Integer, default=0)
    last_updated = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
