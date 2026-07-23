from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Numeric
from app.models.trip import Base

class Flight(Base):
    __tablename__ = "flights"
    id = Column(Integer, primary_key=True, autoincrement=True)
    trip_id = Column(Integer, ForeignKey("trips.id", ondelete="CASCADE"), nullable=False)
    flight_no = Column(String(20), nullable=False)
    airline = Column(String(100), nullable=True)
    departure_city = Column(String(100), nullable=False)
    departure_airport = Column(String(200), nullable=True)
    arrival_city = Column(String(100), nullable=False)
    arrival_airport = Column(String(200), nullable=True)
    departure_time = Column(DateTime, nullable=False)
    arrival_time = Column(DateTime, nullable=False)
    duration_min = Column(Integer, nullable=True)
    price = Column(Numeric(10, 2), nullable=True)
    seat_class = Column(String(50), nullable=True)
    booking_link = Column(String(500), nullable=True)
    notes = Column(Text, nullable=True)
