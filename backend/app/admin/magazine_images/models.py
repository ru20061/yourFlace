from sqlalchemy import Column, BigInteger, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class MagazineImage(Base):
    __tablename__ = "magazine_images"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    magazine_id = Column(BigInteger, ForeignKey('magazines.id'), nullable=False)
    image_id = Column(BigInteger, ForeignKey('images.id'), nullable=False)
    sort_order = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
