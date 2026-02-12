from sqlalchemy import Column, BigInteger, String, Integer, Boolean, Text, TIMESTAMP, Date, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func
from app.database import Base

class ScheduledNotification(Base):
    __tablename__ = "scheduled_notifications"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    notification_template_id = Column(BigInteger, ForeignKey('notification_templates.id'), nullable=False)
    receiver_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    send_at = Column(TIMESTAMP, nullable=False)
    is_sent = Column(Boolean, default=False)
    sent_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
