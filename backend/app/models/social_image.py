from sqlalchemy import Column, Integer, String, ForeignKey
from app.models.trip import Base

class SocialImage(Base):
    __tablename__ = "social_images"
    id = Column(Integer, primary_key=True, autoincrement=True)
    note_id = Column(Integer, ForeignKey("social_notes.id", ondelete="CASCADE"), nullable=False)
    url = Column(String(500), nullable=True)
    url_large = Column(String(500), nullable=True)
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    sort_order = Column(Integer, default=0)
    local_path = Column(String(500), nullable=True)