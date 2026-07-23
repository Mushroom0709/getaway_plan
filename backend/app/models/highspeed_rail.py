from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Numeric
from app.models.trip import Base

class HighspeedRail(Base):
    __tablename__ = "highspeed_rails"
    id = Column(Integer, primary_key=True, autoincrement=True)
    trip_id = Column(Integer, ForeignKey("trips.id", ondelete="CASCADE"), nullable=False)
    train_no = Column(String(20), nullable=False)
    departure_city = Column(String(100), nullable=False)
    departure_station = Column(String(200), nullable=False)
    arrival_city = Column(String(100), nullable=False)
    arrival_station = Column(String(200), nullable=False)
    departure_time = Column(DateTime, nullable=False)
    arrival_time = Column(DateTime, nullable=False)
    duration_min = Column(Integer, nullable=True)
    price = Column(Numeric(10, 2), nullable=True)
    seat_class = Column(String(50), nullable=True)
    booking_link = Column(String(500), nullable=True)
    notes = Column(Text, nullable=True)
