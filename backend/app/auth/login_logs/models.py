from sqlalchemy import Column, BigInteger, String, Integer, Boolean, Text, TIMESTAMP, Date, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func
from app.database import Base

class LoginLog(Base):
    __tablename__ = "login_logs"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=True)
    ip_address = Column(String(45), nullable=True)
    device_type = Column(String(20), nullable=True)
    device_info = Column(Text, nullable=True)
    status = Column(String(20), nullable=False)
    fail_reason = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
