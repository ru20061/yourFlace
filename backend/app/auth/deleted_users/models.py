from sqlalchemy import Column, BigInteger, String, Integer, Boolean, Text, TIMESTAMP, Date, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func
from app.database import Base

class DeletedUser(Base):
    __tablename__ = "deleted_users"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    email = Column(String(255), nullable=False)
    deleted_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    reason = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)
    scheduled_delete_at = Column(TIMESTAMP, nullable=True)
