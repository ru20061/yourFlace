from sqlalchemy import Column, BigInteger, String, Integer, Boolean, Text, TIMESTAMP, Date, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func
from app.database import Base

class CelebCategoryMap(Base):
    __tablename__ = "celeb_category_map"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    celeb_id = Column(BigInteger, ForeignKey('celebs.id'), nullable=False)
    category_id = Column(BigInteger, ForeignKey('celeb_categories.id'), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
