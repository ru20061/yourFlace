from sqlalchemy import Column, BigInteger, String, Integer, Boolean, Text, TIMESTAMP, Date, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func
from app.database import Base

class NotificationTemplate(Base):
    __tablename__ = "notification_templates"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    template_name = Column(String(100), nullable=False)
    noti_type = Column(String(20), nullable=False)
    title_template = Column(String(255), nullable=True)
    message_template = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
