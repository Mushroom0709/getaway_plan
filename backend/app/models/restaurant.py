from sqlalchemy import Column, Integer, String, Text, ForeignKey, Numeric
from app.models.trip import Base

class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, autoincrement=True)
    trip_id = Column(Integer, ForeignKey("trips.id", ondelete="CASCADE"), nullable=False)
    spot_id = Column(Integer, ForeignKey("spots.id", ondelete="SET NULL"), nullable=True)
    city = Column(String(100), nullable=True)
    name = Column(String(200), nullable=False)
    address = Column(String(300), nullable=True)
    lng = Column(Numeric(10, 6), nullable=True)
    lat = Column(Numeric(10, 6), nullable=True)
    rating = Column(Numeric(2, 1), nullable=True)
    avg_price = Column(Numeric(10, 2), nullable=True)
    cuisine = Column(String(100), nullable=True)
    phone = Column(String(50), nullable=True)
    opening_hours = Column(String(200), nullable=True)
    maps_url = Column(String(500), nullable=True)
    cover_image = Column(String(500), nullable=True)
    notes = Column(Text, nullable=True)
