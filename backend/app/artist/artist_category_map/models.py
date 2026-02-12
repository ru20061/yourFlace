from sqlalchemy import Column, BigInteger, String, Integer, Boolean, Text, TIMESTAMP, Date, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func
from app.database import Base

class ArtistCategoryMap(Base):
    __tablename__ = "artist_category_map"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    artist_id = Column(BigInteger, ForeignKey('artists.id'), nullable=False)
    category_id = Column(BigInteger, ForeignKey('artist_categories.id'), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
