from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class FlightCreate(BaseModel):
    flight_no: str
    airline: Optional[str] = None
    departure_city: str
    departure_airport: Optional[str] = None
    arrival_city: str
    arrival_airport: Optional[str] = None
    departure_time: datetime
    arrival_time: datetime
    duration_min: Optional[int] = None
    price: Optional[float] = None
    seat_class: Optional[str] = None
    booking_link: Optional[str] = None
    notes: Optional[str] = None

class FlightUpdate(BaseModel):
    flight_no: Optional[str] = None
    airline: Optional[str] = None
    departure_city: Optional[str] = None
    departure_airport: Optional[str] = None
    arrival_city: Optional[str] = None
    arrival_airport: Optional[str] = None
    departure_time: Optional[datetime] = None
    arrival_time: Optional[datetime] = None
    duration_min: Optional[int] = None
    price: Optional[float] = None
    seat_class: Optional[str] = None
    booking_link: Optional[str] = None
    notes: Optional[str] = None

class FlightResponse(BaseModel):
    id: int
    trip_id: int
    flight_no: str
    airline: Optional[str] = None
    departure_city: str
    departure_airport: Optional[str] = None
    arrival_city: str
    arrival_airport: Optional[str] = None
    departure_time: datetime
    arrival_time: datetime
    duration_min: Optional[int] = None
    price: Optional[float] = None
    seat_class: Optional[str] = None
    booking_link: Optional[str] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True
