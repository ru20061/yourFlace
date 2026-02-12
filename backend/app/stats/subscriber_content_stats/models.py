from sqlalchemy import Column, BigInteger, String, Integer, Boolean, Text, TIMESTAMP, Date, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func
from app.database import Base

class SubscriberContentStat(Base):
    __tablename__ = "subscriber_content_stats"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    subscription_id = Column(BigInteger, ForeignKey('subscriptions.id'), unique=True, nullable=False)
    post_count = Column(Integer, default=0)
    image_count = Column(Integer, default=0)
    fan_like_count = Column(Integer, default=0)
    fan_recommend_count = Column(Integer, default=0)
    last_updated = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
