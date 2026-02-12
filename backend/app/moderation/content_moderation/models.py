from sqlalchemy import Column, BigInteger, String, Integer, Boolean, Text, TIMESTAMP, Date, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func
from app.database import Base

class ContentModeration(Base):
    __tablename__ = "content_moderation"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    content_type = Column(String(20), nullable=False)
    content_id = Column(BigInteger, nullable=False)
    creator_ref_type = Column(String(50), nullable=True)
    creator_ref_id = Column(BigInteger, nullable=True)
    model_id = Column(BigInteger, ForeignKey('moderation_models.id'), nullable=True)
    result = Column(JSON, nullable=True)
    is_flagged = Column(Boolean, default=False)
    flagged_reason = Column(String(100), nullable=True)
    reviewed = Column(Boolean, default=False)
    reviewed_by = Column(BigInteger, ForeignKey('users.id'), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
