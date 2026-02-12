from sqlalchemy import Column, BigInteger, String, Integer, Boolean, Text, TIMESTAMP, Date, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func
from app.database import Base

class SystemMessage(Base):
    __tablename__ = "system_messages"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    target_type = Column(String(20), nullable=True)
    target_id = Column(BigInteger, nullable=True)
    start_at = Column(TIMESTAMP, nullable=True)
    end_at = Column(TIMESTAMP, nullable=True)
    is_active = Column(Boolean, default=True)
    write_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    search_text = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
