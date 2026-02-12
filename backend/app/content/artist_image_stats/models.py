from sqlalchemy import Column, BigInteger, String, Integer, Boolean, Text, TIMESTAMP, Date, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func
from app.database import Base

class ArtistImageStat(Base):
    __tablename__ = "artist_image_stats"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    artist_image_id = Column(BigInteger, ForeignKey('artist_images.id'), unique=True, nullable=False)
    view_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    fan_like_count = Column(Integer, default=0)
    last_updated = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
