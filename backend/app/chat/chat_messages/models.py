from sqlalchemy import Column, BigInteger, String, Integer, Boolean, Text, TIMESTAMP, Date, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func
from app.database import Base

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    chat_room_id = Column(BigInteger, ForeignKey('chat_rooms.id'), nullable=False)
    sender_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    sender_type = Column(String(20), nullable=False)
    message_type = Column(String(20), default='text')
    content = Column(Text, nullable=True)
    is_pinned = Column(Boolean, default=False)
    status = Column(String(20), default='active', nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
