from sqlalchemy import Column, BigInteger, String, Integer, Boolean, Text, TIMESTAMP, Date, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func
from app.database import Base

class Banner(Base):
    __tablename__ = "banners"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    position = Column(String(30), nullable=False)
    title = Column(String(255), nullable=True)
    image_url = Column(String(255), nullable=False)
    link_url = Column(String(255), nullable=True)
    priority = Column(Integer, default=0)
    start_at = Column(TIMESTAMP, nullable=True)
    end_at = Column(TIMESTAMP, nullable=True)
    is_active = Column(Boolean, default=True)
    write_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
