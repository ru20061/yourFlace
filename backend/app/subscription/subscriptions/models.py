from sqlalchemy import Column, BigInteger, String, Integer, Boolean, Text, TIMESTAMP, Date, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func
from app.database import Base

class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    fan_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    artist_id = Column(BigInteger, ForeignKey('artists.id'), nullable=False)
    fan_nickname = Column(String(50), nullable=True)
    fan_profile_image = Column(String(255), nullable=True)
    status = Column(String(20), default='subscribed', nullable=False)
    payments_type = Column(String(20), default='free')
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    search_text = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
