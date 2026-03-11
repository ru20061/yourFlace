from sqlalchemy import Column, BigInteger, String, Text, Date, TIMESTAMP, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from app.database import Base


class Diary(Base):
    __tablename__ = "diaries"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    celeb_id = Column(BigInteger, ForeignKey("celebs.id", ondelete="CASCADE"), nullable=False)
    entry_date = Column(Date, nullable=False)
    content_html = Column(Text, nullable=False, default="")
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

    __table_args__ = (
        # 유저 1명 + 셀럽 1명 + 날짜 1개 → 일기 1건
        UniqueConstraint("user_id", "celeb_id", "entry_date", name="uq_diary_user_celeb_date"),
    )
