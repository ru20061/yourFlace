from sqlalchemy import Column, BigInteger, String, Integer, Boolean, Text, TIMESTAMP, Date, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func
from app.database import Base

class ArtistVideo(Base):
    __tablename__ = "artist_videos"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    artist_id = Column(BigInteger, ForeignKey('artists.id'), nullable=False)
    write_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    write_role = Column(String(20), nullable=False)
    url = Column(String(512), nullable=False)
    thumbnail_url = Column(String(512), nullable=True)
    title = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    size_bytes = Column(BigInteger, nullable=True)
    mime_type = Column(String(50), nullable=True)
    published_date = Column(Date, nullable=True)
    tags = Column(JSON, nullable=True)
    visibility = Column(String(20), default='public')
    is_visible = Column(Boolean, default=True)
    search_text = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
