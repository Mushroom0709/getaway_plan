from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Numeric, Time, Enum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.models.trip import Base
import enum

class SpotCategory(str, enum.Enum):
    airport = "airport"
    highspeed_rail = "highspeed_rail"
    train = "train"
    scenic = "scenic"
    photo = "photo"
    hotel = "hotel"
    restaurant = "restaurant"
    other = "other"

class Spot(Base):
    __tablename__ = "spots"

    id = Column(Integer, primary_key=True, autoincrement=True)
    trip_id = Column(Integer, ForeignKey("trips.id", ondelete="CASCADE"), nullable=False)
    day_id = Column(Integer, ForeignKey("days.id", ondelete="SET NULL"), nullable=True)
    name = Column(String(200), nullable=False)
    lng = Column(Numeric(10, 6), nullable=False)
    lat = Column(Numeric(10, 6), nullable=False)
    category = Column(Enum(SpotCategory), nullable=False, default=SpotCategory.other)
    is_nav_point = Column(Boolean, default=False)
    nav_order = Column(Integer, nullable=True)
    arrival_time = Column(Time, nullable=True)
    description = Column(String(500), nullable=True)
    intro = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
