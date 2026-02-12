from sqlalchemy import Column, BigInteger, String, Integer, Boolean, Text, TIMESTAMP, Date, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func
from app.database import Base

class NotificationSetting(Base):
    __tablename__ = "notification_settings"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    subscription_id = Column(BigInteger, ForeignKey('subscriptions.id'), nullable=True)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    source_type = Column(String(20), nullable=True)
    notify_all = Column(Boolean, default=True)
    notify_post = Column(Boolean, default=True)
    notify_comment = Column(Boolean, default=True)
    notify_reply = Column(Boolean, default=True)
    notify_notice = Column(Boolean, default=True)
    notify_payment = Column(Boolean, default=True)
    notify_warning = Column(Boolean, default=True)
    receive_app = Column(Boolean, default=True)
    receive_push = Column(Boolean, default=True)
    receive_email = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
