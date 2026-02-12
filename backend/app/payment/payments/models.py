from sqlalchemy import Column, BigInteger, String, Integer, Boolean, Text, TIMESTAMP, Date, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func
from app.database import Base

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    payment_type = Column(String(50), nullable=False)
    related_id = Column(BigInteger, nullable=True)
    related_type = Column(String(50), nullable=True)
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(10), default='KRW')
    status = Column(String(20), default='pending')
    transaction_id = Column(String(255), nullable=True)
    payment_method_id = Column(BigInteger, ForeignKey('payment_methods.id'), nullable=True)
    paid_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
