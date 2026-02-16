from sqlalchemy import Column, BigInteger, String, Boolean, Text, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func
from app.database import Base

class Magazine(Base):
    __tablename__ = "magazines"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(280), unique=True, nullable=True, index=True)
    content = Column(Text, nullable=False)
    summary = Column(String(500), nullable=True)
    thumbnail_url = Column(String(255), nullable=True)
    category = Column(String(50), nullable=True)
    artist_id = Column(BigInteger, ForeignKey('artists.id'), nullable=True)
    write_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    tags = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True)
    view_count = Column(BigInteger, default=0)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
