from sqlalchemy import Column, BigInteger, String, Integer, Boolean, Text, TIMESTAMP, Date, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func
from app.database import Base

class UserSetting(Base):
    __tablename__ = "user_settings"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id'), unique=True, nullable=False)
    language = Column(String(10), default='ko')
    theme = Column(String(20), default='light')
    show_profile = Column(Boolean, default=True)
    show_birth_date = Column(Boolean, default=True)
    show_activity_status = Column(Boolean, default=True)
    receive_system_notice = Column(Boolean, default=True)
    receive_system_app = Column(Boolean, default=True)
    receive_system_push = Column(Boolean, default=True)
    receive_system_email = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
