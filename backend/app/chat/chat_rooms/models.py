from sqlalchemy import Column, BigInteger, String, Integer, Boolean, Text, TIMESTAMP, Date, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func
from app.database import Base

class ChatRoom(Base):
    __tablename__ = "chat_rooms"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    room_type = Column(String(20), nullable=False)
    artist_id = Column(BigInteger, ForeignKey('artists.id'), nullable=True)
    room_name = Column(String(255), nullable=True)
    room_image = Column(String(512), nullable=True)
    last_message_at = Column(TIMESTAMP, nullable=True)
    status = Column(String(20), default='active', nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
