from sqlalchemy import Column, BigInteger, String, Integer, Boolean, Text, TIMESTAMP, Date, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func
from app.database import Base

class ChatVideo(Base):
    __tablename__ = "chat_videos"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    chat_message_id = Column(BigInteger, ForeignKey('chat_messages.id'), nullable=False)
    url = Column(String(512), nullable=False)
    thumbnail_url = Column(String(512), nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    size_bytes = Column(BigInteger, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
