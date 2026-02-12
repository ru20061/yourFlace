from sqlalchemy import Column, BigInteger, String, Integer, Boolean, Text, TIMESTAMP, Date, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func
from app.database import Base

class ChatReport(Base):
    __tablename__ = "chat_reports"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    chat_message_id = Column(BigInteger, ForeignKey('chat_messages.id'), nullable=False)
    reported_by = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    reason = Column(String(255), nullable=True)
    status = Column(String(20), default='pending')
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
