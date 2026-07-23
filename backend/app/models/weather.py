from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from app.models.trip import Base

class Weather(Base):
    __tablename__ = "weather"
    id = Column(Integer, primary_key=True, autoincrement=True)
    trip_id = Column(Integer, ForeignKey("trips.id", ondelete="CASCADE"), nullable=False)
    city = Column(String(100), nullable=False)
    date = Column(Date, nullable=False)
    high_temp = Column(String(20), nullable=True)
    low_temp = Column(String(20), nullable=True)
    weather_desc = Column(String(200), nullable=True)
    advice = Column(Text, nullable=True)