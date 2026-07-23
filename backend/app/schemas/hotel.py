from pydantic import BaseModel
from datetime import date
from typing import Optional

class HotelCreate(BaseModel):
    spot_id: Optional[int] = None
    city: str
    name: str
    brand: Optional[str] = None
    rating: Optional[float] = None
    opened_year: Optional[int] = None
    price_per_room: Optional[float] = None
    room_type: Optional[str] = None
    features: Optional[list[str]] = None
    check_in_date: Optional[date] = None
    check_out_date: Optional[date] = None
    lng: Optional[float] = None
    lat: Optional[float] = None
    phone: Optional[str] = None
    cover_image: Optional[str] = None
    notes: Optional[str] = None

class HotelUpdate(BaseModel):
    spot_id: Optional[int] = None
    city: Optional[str] = None
    name: Optional[str] = None
    brand: Optional[str] = None
    rating: Optional[float] = None
    opened_year: Optional[int] = None
    price_per_room: Optional[float] = None
    room_type: Optional[str] = None
    features: Optional[list[str]] = None
    check_in_date: Optional[date] = None
    check_out_date: Optional[date] = None
    lng: Optional[float] = None
    lat: Optional[float] = None
    phone: Optional[str] = None
    cover_image: Optional[str] = None
    notes: Optional[str] = None

class HotelResponse(BaseModel):
    id: int
    trip_id: int
    spot_id: Optional[int] = None
    city: str
    name: str
    brand: Optional[str] = None
    rating: Optional[float] = None
    opened_year: Optional[int] = None
    price_per_room: Optional[float] = None
    room_type: Optional[str] = None
    features: Optional[list[str]] = None
    check_in_date: Optional[date] = None
    check_out_date: Optional[date] = None
    lng: Optional[float] = None
    lat: Optional[float] = None
    phone: Optional[str] = None
    cover_image: Optional[str] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True
