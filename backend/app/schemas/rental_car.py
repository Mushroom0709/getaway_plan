from pydantic import BaseModel
from typing import Optional

class RentalCarCreate(BaseModel):
    platform: Optional[str] = None
    car_name: str
    daily_price: Optional[float] = None
    engine: Optional[str] = None
    seats: Optional[int] = None
    trunk: Optional[str] = None
    notes: Optional[str] = None

class RentalCarUpdate(BaseModel):
    platform: Optional[str] = None
    car_name: Optional[str] = None
    daily_price: Optional[float] = None
    engine: Optional[str] = None
    seats: Optional[int] = None
    trunk: Optional[str] = None
    notes: Optional[str] = None

class RentalCarResponse(BaseModel):
    id: int
    trip_id: int
    platform: Optional[str] = None
    car_name: str
    daily_price: Optional[float] = None
    engine: Optional[str] = None
    seats: Optional[int] = None
    trunk: Optional[str] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True
