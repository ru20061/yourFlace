from sqlalchemy import Column, BigInteger, String, Integer, Boolean, Text, TIMESTAMP, Date, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func
from app.database import Base

class SubscriptionBlacklist(Base):
    __tablename__ = "subscription_blacklist"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    actor_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    actor_role = Column(String(20), nullable=False)
    target_user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    reason = Column(String(255), nullable=True)
    status = Column(String(20), default='active', nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
