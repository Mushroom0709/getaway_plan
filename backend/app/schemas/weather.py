from pydantic import BaseModel
from typing import Optional
from datetime import date

class WeatherCreate(BaseModel):
    city: str
    date: date
    high_temp: Optional[str] = None
    low_temp: Optional[str] = None
    weather_desc: Optional[str] = None
    advice: Optional[str] = None

class WeatherUpdate(BaseModel):
    city: Optional[str] = None
    date: Optional[date] = None
    high_temp: Optional[str] = None
    low_temp: Optional[str] = None
    weather_desc: Optional[str] = None
    advice: Optional[str] = None

class WeatherResponse(BaseModel):
    id: int
    trip_id: int
    city: str
    date: date
    high_temp: Optional[str] = None
    low_temp: Optional[str] = None
    weather_desc: Optional[str] = None
    advice: Optional[str] = None

    class Config:
        from_attributes = True