from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Enum
from sqlalchemy.orm import DeclarativeBase, relationship
from datetime import datetime, timezone
import enum

class Base(DeclarativeBase):
    pass

class TripStatus(str, enum.Enum):
    planning = "planning"
    active = "active"
    completed = "completed"

class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    status = Column(Enum(TripStatus), default=TripStatus.planning, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    days = relationship("Day", back_populates="trip", lazy="selectin", cascade="all, delete-orphan")
