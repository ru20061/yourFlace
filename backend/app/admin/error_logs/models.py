from sqlalchemy import Column, BigInteger, String, Integer, Boolean, Text, TIMESTAMP, Date, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func
from app.database import Base

class ErrorLog(Base):
    __tablename__ = "error_logs"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    error_type = Column(String(100), nullable=False)
    message = Column(Text, nullable=True)
    stack_trace = Column(Text, nullable=True)
    severity = Column(String(20), nullable=False)
    source_module = Column(String(100), nullable=True)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=True)
    resolved = Column(Boolean, default=False)
    resolved_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
