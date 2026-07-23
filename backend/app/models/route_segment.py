from sqlalchemy import Column, Integer, String, Text, ForeignKey, Numeric
from app.models.trip import Base

class RouteSegment(Base):
    __tablename__ = "route_segments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    trip_id = Column(Integer, ForeignKey("trips.id", ondelete="CASCADE"), nullable=False)
    from_spot_id = Column(Integer, ForeignKey("spots.id", ondelete="SET NULL"), nullable=True)
    to_spot_id = Column(Integer, ForeignKey("spots.id", ondelete="SET NULL"), nullable=True)
    distance_km = Column(Numeric(8, 2), nullable=True)
    duration_min = Column(Integer, nullable=True)
    polyline = Column(Text, nullable=True)
    color = Column(String(20), nullable=True)
    day_number = Column(Integer, nullable=True)
    route_type = Column(String(20), nullable=False, default="driving")  # "driving" or "transit"
