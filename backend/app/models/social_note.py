from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship
from app.models.trip import Base
import enum
from datetime import datetime, timezone

class Platform(str, enum.Enum):
    xiaohongshu = "xiaohongshu"
    douyin = "douyin"

class SocialNote(Base):
    __tablename__ = "social_notes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    spot_id = Column(Integer, ForeignKey("spots.id", ondelete="CASCADE"), nullable=False)
    platform = Column(SAEnum(Platform), nullable=False)
    note_id = Column(String(100), nullable=False)
    title = Column(String(500), nullable=True)
    author = Column(String(200), nullable=True)
    author_id = Column(String(100), nullable=True)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    description = Column(Text, nullable=True)
    xsec_token = Column(String(200), nullable=True)
    source_url = Column(String(500), nullable=True)
    note_type = Column(String(50), nullable=True)
    fetched_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    images = relationship("SocialImage", backref="note", lazy="selectin", cascade="all, delete-orphan")