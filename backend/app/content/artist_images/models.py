from sqlalchemy import Column, BigInteger, String, Integer, Boolean, Text, TIMESTAMP, Date, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func
from app.database import Base

class ArtistImage(Base):
    __tablename__ = "artist_images"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    artist_id = Column(BigInteger, ForeignKey('artists.id'), nullable=False)
    image_id = Column(BigInteger, ForeignKey('images.id'), nullable=False)
    write_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    write_role = Column(String(20), nullable=False)
    image_purpose = Column(String(50), nullable=True)
    published_date = Column(Date, nullable=True)
    tags = Column(JSON, nullable=True)
    visibility = Column(String(20), default='public')
    is_visible = Column(Boolean, default=True)
    search_text = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
