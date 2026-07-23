from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Numeric, JSON
from app.models.trip import Base

class Attraction(Base):
    __tablename__ = "attractions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    spot_id = Column(Integer, ForeignKey("spots.id", ondelete="CASCADE"), nullable=False, unique=True)
    ticket_price = Column(String(100), nullable=True)
    opening_hours = Column(String(200), nullable=True)
    best_season = Column(String(200), nullable=True)
    best_time_of_day = Column(String(100), nullable=True)
    duration_hours = Column(Numeric(3, 1), nullable=True)
    altitude = Column(Integer, nullable=True)
    tips = Column(Text, nullable=True)
    highlights = Column(JSON, nullable=True)
    must_see = Column(Boolean, default=False)