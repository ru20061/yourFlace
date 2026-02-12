from sqlalchemy import Column, BigInteger, String, Integer, Boolean, Text, TIMESTAMP, Date, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func
from app.database import Base

class GlobalBlacklist(Base):
    __tablename__ = "global_blacklist"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    admin_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    target_user_id = Column(BigInteger, ForeignKey('users.id'), unique=True, nullable=False)
    reason = Column(String(255), nullable=True)
    status = Column(String(20), default='active', nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
