from pydantic import BaseModel
from datetime import date
from typing import Optional

class DayCreate(BaseModel):
    day_number: int
    date: Optional[date] = None
    title: Optional[str] = None
    drive_hours: Optional[float] = None
    hotel_city: Optional[str] = None
    sort_order: int = 0

class DayUpdate(BaseModel):
    day_number: Optional[int] = None
    date: Optional[date] = None
    title: Optional[str] = None
    drive_hours: Optional[float] = None
    hotel_city: Optional[str] = None
    sort_order: Optional[int] = None

class DayResponse(BaseModel):
    id: int
    trip_id: int
    day_number: int
    date: Optional[date] = None
    title: Optional[str] = None
    drive_hours: Optional[float] = None
    hotel_city: Optional[str] = None
    sort_order: int

    class Config:
        from_attributes = True
