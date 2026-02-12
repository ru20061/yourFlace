from sqlalchemy import Column, BigInteger, String, Integer, Boolean, Text, TIMESTAMP, Date, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func
from app.database import Base

class ChatPin(Base):
    __tablename__ = "chat_pins"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    chat_room_id = Column(BigInteger, ForeignKey('chat_rooms.id'), nullable=False)
    chat_message_id = Column(BigInteger, ForeignKey('chat_messages.id'), nullable=False)
    pinned_by = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
