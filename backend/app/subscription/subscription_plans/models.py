from sqlalchemy import Column, BigInteger, String, Integer, Boolean, Text, TIMESTAMP, Date, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func
from app.database import Base

class SubscriptionPlan(Base):
    __tablename__ = "subscription_plans"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    artist_id = Column(BigInteger, ForeignKey('artists.id'), nullable=False)
    name = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), default=0)
    currency = Column(String(10), default='KRW')
    billing_cycle = Column(String(20), default='monthly')
    duration_days = Column(Integer, nullable=True)
    benefits = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
