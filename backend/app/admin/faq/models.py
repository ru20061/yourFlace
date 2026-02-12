from sqlalchemy import Column, BigInteger, String, Integer, Boolean, Text, TIMESTAMP, Date, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func
from app.database import Base

class FAQ(Base):
    __tablename__ = "faq"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    category = Column(String(50), nullable=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    priority = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    write_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    search_text = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
