from sqlalchemy import Column, BigInteger, String, Integer, Boolean, Text, TIMESTAMP, Date, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func
from app.database import Base

class ChatImage(Base):
    __tablename__ = "chat_images"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    chat_message_id = Column(BigInteger, ForeignKey('chat_messages.id'), nullable=False)
    image_id = Column(BigInteger, ForeignKey('images.id'), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
