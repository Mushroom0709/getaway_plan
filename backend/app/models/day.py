from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.models.trip import Base

class Day(Base):
    __tablename__ = "days"

    id = Column(Integer, primary_key=True, autoincrement=True)
    trip_id = Column(Integer, ForeignKey("trips.id", ondelete="CASCADE"), nullable=False)
    day_number = Column(Integer, nullable=False)
    date = Column(Date, nullable=True)
    title = Column(String(200), nullable=True)
    drive_hours = Column(Numeric(3, 1), nullable=True)
    hotel_city = Column(String(100), nullable=True)
    sort_order = Column(Integer, nullable=False, default=0)

    trip = relationship("Trip", back_populates="days")
