from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class TripCreate(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

class TripUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[str] = None

class DayResponse(BaseModel):
    id: int
    day_number: int
    date: Optional[date] = None
    title: Optional[str] = None
    drive_hours: Optional[float] = None
    hotel_city: Optional[str] = None
    sort_order: int

    class Config:
        from_attributes = True

class TripResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: str
    created_at: datetime
    updated_at: datetime
    days: list[DayResponse] = []

    class Config:
        from_attributes = True

class TripListResponse(BaseModel):
    id: int
    name: str
    status: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    created_at: datetime

    class Config:
        from_attributes = True
