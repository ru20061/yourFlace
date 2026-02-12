from sqlalchemy import Column, BigInteger, String, Integer, Boolean, Text, TIMESTAMP, Date, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func
from app.database import Base

class Event(Base):
    __tablename__ = "events"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    artist_id = Column(BigInteger, ForeignKey('artists.id'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    event_type = Column(String(50), nullable=True)
    event_date = Column(TIMESTAMP, nullable=True)
    location = Column(Text, nullable=True)
    max_participants = Column(Integer, nullable=True)
    current_participants = Column(Integer, default=0)
    registration_start = Column(TIMESTAMP, nullable=True)
    registration_end = Column(TIMESTAMP, nullable=True)
    status = Column(String(20), default='active', nullable=False)
    search_text = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
