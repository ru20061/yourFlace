from sqlalchemy import Column, BigInteger, String, Integer, Boolean, Text, TIMESTAMP, Date, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func
from app.database import Base

class Artist(Base):
    __tablename__ = "artists"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id'), unique=True, nullable=False)
    stage_name = Column(String(100), nullable=False)
    slug = Column(String(120), unique=True, nullable=True, index=True)
    notes = Column(Text, nullable=True)
    profile_image = Column(String(255), nullable=True)
    cover_image = Column(String(255), nullable=True)
    status = Column(String(20), default='active', nullable=False)
    search_text = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
