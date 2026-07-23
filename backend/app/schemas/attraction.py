from pydantic import BaseModel
from typing import Optional, List

class AttractionCreate(BaseModel):
    ticket_price: Optional[str] = None
    opening_hours: Optional[str] = None
    best_season: Optional[str] = None
    best_time_of_day: Optional[str] = None
    duration_hours: Optional[float] = None
    altitude: Optional[int] = None
    tips: Optional[str] = None
    highlights: Optional[List[str]] = None
    must_see: bool = False

class AttractionUpdate(BaseModel):
    ticket_price: Optional[str] = None
    opening_hours: Optional[str] = None
    best_season: Optional[str] = None
    best_time_of_day: Optional[str] = None
    duration_hours: Optional[float] = None
    altitude: Optional[int] = None
    tips: Optional[str] = None
    highlights: Optional[List[str]] = None
    must_see: Optional[bool] = None

class AttractionResponse(BaseModel):
    id: int
    spot_id: int
    ticket_price: Optional[str] = None
    opening_hours: Optional[str] = None
    best_season: Optional[str] = None
    best_time_of_day: Optional[str] = None
    duration_hours: Optional[float] = None
    altitude: Optional[int] = None
    tips: Optional[str] = None
    highlights: Optional[List[str]] = None
    must_see: bool = False

    class Config:
        from_attributes = True
