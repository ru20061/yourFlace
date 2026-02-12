from sqlalchemy import Column, BigInteger, String, Integer, Boolean, Text, TIMESTAMP, Date, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func
from app.database import Base

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    author_id = Column(BigInteger, nullable=False)
    author_type = Column(String(20), nullable=False)
    content = Column(Text, nullable=True)
    write_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    write_role = Column(String(20), nullable=False)
    visibility = Column(String(20), default='public')
    is_visible = Column(Boolean, default=True)
    is_artist_post = Column(Boolean, default=False)
    published_date = Column(Date, nullable=True)
    tags = Column(JSON, nullable=True)
    title_field = Column(String(255), nullable=True)
    search_text = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
