from sqlalchemy import Column, BigInteger, String, Integer, Boolean, Text, TIMESTAMP, Date, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func
from app.database import Base

class UserAddress(Base):
    __tablename__ = "user_addresses"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    address_name = Column(String(50), nullable=True)
    recipient_name = Column(String(100), nullable=False)
    recipient_phone = Column(String(20), nullable=False)
    postal_code = Column(String(10), nullable=False)
    base_address = Column(String(255), nullable=False)
    detail_address = Column(String(255), nullable=True)
    is_default = Column(Boolean, default=False)
    status = Column(String(10), default='A', server_default='A', nullable=False)
    memo = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
