from sqlalchemy import Column, BigInteger, String, Integer, Boolean, Text, TIMESTAMP, Date, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func
from app.database import Base

class EventAttendance(Base):
    __tablename__ = "event_attendance"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    event_id = Column(BigInteger, ForeignKey('events.id'), nullable=False)
    participant_id = Column(BigInteger, ForeignKey('event_participants.id'), nullable=False)
    checked_in_at = Column(TIMESTAMP, server_default=func.now())
    checked_in_by = Column(BigInteger, ForeignKey('users.id'), nullable=True)
