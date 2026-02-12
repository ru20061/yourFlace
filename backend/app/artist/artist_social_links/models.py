from sqlalchemy import Column, BigInteger, String, Integer, Boolean, Text, TIMESTAMP, Date, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func
from app.database import Base

class ArtistSocialLink(Base):
    __tablename__ = "artist_social_links"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    artist_id = Column(BigInteger, ForeignKey('artists.id'), nullable=False)
    platform_name = Column(String(50), nullable=False)
    url = Column(String(255), nullable=False)
    display_name = Column(String(100), nullable=True)
    follower_count = Column(Integer, default=0)
    priority = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
