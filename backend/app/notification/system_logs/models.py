from sqlalchemy import Column, BigInteger, String, Integer, Boolean, Text, TIMESTAMP, Date, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func
from app.database import Base

class SystemLog(Base):
    __tablename__ = "system_logs"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    scheduled_notification_id = Column(BigInteger, ForeignKey('scheduled_notifications.id'), nullable=True)
    sender_id = Column(BigInteger, ForeignKey('users.id'), nullable=True)
    receiver_id = Column(BigInteger, ForeignKey('users.id'), nullable=True)
    channel = Column(String(20), nullable=True)
    status = Column(String(20), nullable=False)
    error_message = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
