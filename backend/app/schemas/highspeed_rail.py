from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class HighspeedRailCreate(BaseModel):
    train_no: str
    departure_city: str
    departure_station: str
    arrival_city: str
    arrival_station: str
    departure_time: datetime
    arrival_time: datetime
    duration_min: Optional[int] = None
    price: Optional[float] = None
    seat_class: Optional[str] = None
    booking_link: Optional[str] = None
    notes: Optional[str] = None

class HighspeedRailUpdate(BaseModel):
    train_no: Optional[str] = None
    departure_city: Optional[str] = None
    departure_station: Optional[str] = None
    arrival_city: Optional[str] = None
    arrival_station: Optional[str] = None
    departure_time: Optional[datetime] = None
    arrival_time: Optional[datetime] = None
    duration_min: Optional[int] = None
    price: Optional[float] = None
    seat_class: Optional[str] = None
    booking_link: Optional[str] = None
    notes: Optional[str] = None

class HighspeedRailResponse(BaseModel):
    id: int
    trip_id: int
    train_no: str
    departure_city: str
    departure_station: str
    arrival_city: str
    arrival_station: str
    departure_time: datetime
    arrival_time: datetime
    duration_min: Optional[int] = None
    price: Optional[float] = None
    seat_class: Optional[str] = None
    booking_link: Optional[str] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True
