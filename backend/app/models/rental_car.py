from sqlalchemy import Column, Integer, String, Text, ForeignKey, Numeric
from app.models.trip import Base

class RentalCar(Base):
    __tablename__ = "rental_cars"
    id = Column(Integer, primary_key=True, autoincrement=True)
    trip_id = Column(Integer, ForeignKey("trips.id", ondelete="CASCADE"), nullable=False)
    platform = Column(String(100), nullable=True)
    car_name = Column(String(200), nullable=False)
    daily_price = Column(Numeric(10, 2), nullable=True)
    engine = Column(String(100), nullable=True)
    seats = Column(Integer, nullable=True)
    trunk = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
