from sqlalchemy import Column, BigInteger, String, Integer, Boolean, Text, TIMESTAMP, Date, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func
from app.database import Base

class SubscriptionCancellation(Base):
    __tablename__ = "subscription_cancellations"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    subscription_id = Column(BigInteger, ForeignKey('subscriptions.id'), nullable=False)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    artist_id = Column(BigInteger, ForeignKey('artists.id'), nullable=False)
    reason_code = Column(String(50), nullable=True)
    reason_detail = Column(Text, nullable=True)
    cancelled_at = Column(TIMESTAMP, server_default=func.now())
    subscription_started_at = Column(TIMESTAMP, nullable=True)
    refund_amount = Column(Numeric(10, 2), default=0)
    is_refunded = Column(Boolean, default=False)
